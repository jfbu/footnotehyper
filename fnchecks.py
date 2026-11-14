#!/usr/bin/env python3
"""Generic sanity checks on the footnote structures of a tagged PDF.

Usage: fnchecks.py [--list] file.pdf ...

Needs structtree.py in the same directory (text extraction, role maps).

Structure types are compared after resolution through the role maps, so the
checks do not depend on the names chosen by LaTeX (footnote, footnotemark,
footnotelabel, ...).  A note is a structure of type FENote (PDF 2.0) or Note
(PDF 1.7).  A mark is a structure which is not a note and is linked to a
note by a /Ref entry, in either direction.

  NOLBL    a note without Lbl child
  LBLS     a note with more than one Lbl child
  LBLPOS   the Lbl of a note is not its first child
  MCKID    marked content (MCID) directly inside a note; not a defect: the
           kernel puts the text of a note inside paragraph structures,
           except with the para option of footmisc
  NOTEXT   a note without text outside of its Lbl
  NEST     a note inside a note
  NOREF    a note to which no mark is linked by /Ref
  ONEWAY   a /Ref between a note and a mark which exists in one direction
           only
  MARKTXT  the text of a mark differs from the text of the Lbl of its note;
           punctuation at their ends is ignored (babel-french labels are
           like "1.")
  NODEST   the link of a mark has a destination name which is not defined
  DPAGE    the destination of the link of a mark is not on the page of the
           Lbl of its note
  SDEST    the structure destination (/SD) of the link of a mark is not
           inside its note
  DUPMC    a marked content (page, MCID) referenced more than once by the
           structure tree
  ORPHMC   a marked content with MCID in a page which is not referenced by
           the structure tree
  UNTAGGED text in a page outside of any marked content (neither tagged nor
           artifact); typical of material typeset while tagging was
           suspended and nevertheless output
  COUNT    numbers of notes, marks, and links inside marks (always printed)

The last three checks are on the whole document, not only on footnotes.

With --list, one line per note is printed before the messages:
    NOTE  p<page> mark 'text' ... -> p<page> label 'text' : 'start of text'

Parent-child legality itself is checked by tagpdf, not here.

Exit status: 0 if only NOTE, MCKID and COUNT lines were printed, 1 if there
was any other message (including NOTAGGED for a PDF without structure tree),
2 for a usage error, 3 if pikepdf is not available (nothing checked).
"""
import sys
try:
    import pikepdf
except ImportError:
    print("fnchecks.py: pikepdf is not available, no check done")
    sys.exit(3)
from structtree import as_list, link_action, page_mcid_text, resolve_role

NOTE_TYPES = ("FENote", "Note")


def is_int(x):
    return isinstance(x, int) or (isinstance(x, pikepdf.Object)
                                  and x._type_code == pikepdf.ObjectType.integer)


def is_elem(x):
    return isinstance(x, pikepdf.Dictionary) and "/S" in x


def is_mc(x):
    return is_int(x) or (isinstance(x, pikepdf.Dictionary)
                         and x.get("/Type") == "/MCR")


def untagged_text(pdf):
    """List of (page number, number of text operators outside marked content)."""
    out = []
    for i, page in enumerate(pdf.pages):
        depth = n = 0
        for operands, op in pikepdf.parse_content_stream(page):
            name = str(op)
            if name in ("BDC", "BMC"):
                depth += 1
            elif name == "EMC":
                depth = max(0, depth - 1)
            elif depth == 0 and name in ("Tj", "TJ", "'", '"'):
                n += 1
        if n:
            out.append((i + 1, n))
    return out


def named_dests(pdf):
    """Map destination name -> objgen of its page."""
    out = {}

    def add(name, val):
        if isinstance(val, pikepdf.Dictionary):
            val = val.get("/D")
        if isinstance(val, pikepdf.Array) and len(val) \
                and isinstance(val[0], pikepdf.Dictionary):
            out[str(name)] = val[0].objgen
        else:
            out[str(name)] = None

    names = pdf.Root.get("/Names")
    if names is not None and "/Dests" in names:
        for k, v in pikepdf.NameTree(names.Dests).items():
            add(k, v)
    old = pdf.Root.get("/Dests")
    if old is not None:
        for k, v in old.items():
            add(k[1:], v)
    return out


def check(path, listing):
    pdf = pikepdf.open(path)
    root = pdf.Root.get("/StructTreeRoot")
    if root is None:
        return ["NOTAGGED"]
    rolemap = root.get("/RoleMap")
    texts = page_mcid_text(pdf)
    pageno = {p.obj.objgen: i + 1 for i, p in enumerate(pdf.pages)}
    dests = named_dests(pdf)
    std_cache = {}

    def std(e):
        if "/S" not in e:
            return "StructTreeRoot"
        key = e.objgen if e.is_indirect else id(e)
        if key not in std_cache:
            std_cache[key] = resolve_role(str(e.S)[1:], e.get("/NS"), rolemap)[0]
        return std_cache[key]

    def label(e):
        if "/S" not in e:
            return "StructTreeRoot"
        n, s = str(e.S)[1:], std(e)
        return n if n == s else f"{n}->{s}"

    def is_note(e):
        return is_elem(e) and std(e) in NOTE_TYPES

    def same(a, b):
        return a.is_indirect and b.is_indirect and a.objgen == b.objgen

    def contents(e, page, skip, guard=None):
        """(page objgen, mcid) or link annotation of e, in document order."""
        guard = set() if guard is None else guard
        if e.is_indirect:
            if e.objgen in guard:
                return
            guard.add(e.objgen)
        if "/Pg" in e:
            page = e.Pg.objgen
        for k in as_list(e.get("/K")):
            if is_int(k):
                yield (page, int(k))
            elif not isinstance(k, pikepdf.Dictionary):
                continue
            elif k.get("/Type") == "/MCR":
                if "/Stm" not in k:
                    yield (k.Pg.objgen if "/Pg" in k else page, int(k.MCID))
            elif k.get("/Type") == "/OBJR":
                obj = k.get("/Obj")
                if isinstance(obj, pikepdf.Dictionary) \
                        and obj.get("/Subtype") == "/Link":
                    yield obj
            elif "/S" in k and not skip(k):
                yield from contents(k, page, skip, guard)

    def inherited_page(e):
        seen = set()
        while isinstance(e, pikepdf.Dictionary) and "/S" in e:
            if "/Pg" in e:
                return e.Pg.objgen
            if e.is_indirect:
                if e.objgen in seen:
                    break
                seen.add(e.objgen)
            e = e.get("/P")
        return None

    def text_page(e, skip=lambda k: False):
        """(text, page number of the first marked content) of e."""
        parts, page = [], None
        for c in contents(e, inherited_page(e), skip):
            if isinstance(c, tuple):
                if page is None:
                    page = pageno.get(c[0])
                parts.append(texts.get(c, ""))
        return " ".join(" ".join(parts).split()), page

    def links(e):
        return [c for c in contents(e, None, is_note)
                if not isinstance(c, tuple)]

    def inside(e, anc):
        seen = set()
        while isinstance(e, pikepdf.Dictionary) and "/S" in e:
            if same(e, anc):
                return True
            if e.is_indirect:
                if e.objgen in seen:
                    return False
                seen.add(e.objgen)
            e = e.get("/P")
        return False

    def refs(e):
        return [r for r in as_list(e.get("/Ref")) if is_elem(r)]

    def squeeze(s):
        return "".join(s.split()).strip(".,:;()[]")

    def short(s, n=40):
        return s if len(s) <= n else s[:n - 3] + "..."

    msgs, lines = [], []
    notes, marks = [], {}
    visited = set()

    def visit(e, parent, in_note):
        if e.is_indirect:
            if e.objgen in visited:
                return
            visited.add(e.objgen)
        note = is_note(e)
        if note:
            notes.append((e, parent, in_note))
        elif any(is_note(r) for r in refs(e)) and e.is_indirect:
            marks[e.objgen] = e
        for k in as_list(e.get("/K")):
            if is_elem(k):
                visit(k, e, in_note or note)

    for k in as_list(root.get("/K")):
        if is_elem(k):
            visit(k, root, False)

    nlinks = 0
    for note, parent, in_note in notes:
        raw = as_list(note.get("/K"))
        lbls = [k for k in raw if is_elem(k) and std(k) == "Lbl"]
        ltext, lpage = text_page(lbls[0]) if lbls else ("", None)
        ntext, npage = text_page(
            note, lambda k: is_note(k) or (std(k) == "Lbl"
                                           and any(same(k, x) for x in lbls)))
        where = f"{ltext!r} (p{lpage or npage or '?'}) under <{label(parent)}>"
        if not lbls:
            msgs.append(f"NOLBL   note {where}")
        elif len(lbls) > 1:
            msgs.append(f"LBLS    note {where} has {len(lbls)} Lbl")
        elif not (is_elem(raw[0]) and same(raw[0], lbls[0])):
            msgs.append(f"LBLPOS  note {where}")
        if any(is_mc(k) for k in raw):
            msgs.append(f"MCKID   marked content child of note {where}")
        if not ntext:
            msgs.append(f"NOTEXT  note {where}")
        if in_note:
            msgs.append(f"NEST    note {where}")
        mrefs = refs(note)
        for m in mrefs:
            if not is_note(m) and m.is_indirect:
                marks[m.objgen] = m
        if not mrefs:
            msgs.append(f"NOREF   note {where}")
        mdescr = []
        for m in mrefs:
            mtext, mpage = text_page(m, is_note)
            mdescr.append(f"p{mpage or '?'} mark {mtext!r}")
            if not any(same(r, note) for r in refs(m)):
                msgs.append(f"ONEWAY  note {where} -> <{label(m)}> {mtext!r}")
            if lbls and squeeze(mtext) != squeeze(ltext):
                msgs.append(f"MARKTXT mark {mtext!r} (p{mpage or '?'}) "
                            f"for note {where}")
            for annot in links(m):
                nlinks += 1
                name, sd = link_action(annot)
                if name is not None:
                    if name not in dests:
                        msgs.append(f"NODEST  {name!r}, mark {mtext!r} "
                                    f"of note {where}")
                    elif lpage is not None \
                            and pageno.get(dests[name]) != lpage:
                        msgs.append(f"DPAGE   {name!r} on "
                                    f"p{pageno.get(dests[name], '?')}, "
                                    f"mark {mtext!r} of note {where}")
                if sd is not None and not inside(sd, note):
                    msgs.append(f"SDEST   <{label(sd)}>, mark {mtext!r} "
                                f"of note {where}")
        lines.append("NOTE  " + (", ".join(mdescr) or "no mark")
                     + f" -> p{lpage or npage or '?'} label {ltext!r}"
                     + f" : {short(ntext)!r}")

    for m in marks.values():
        mtext, mpage = text_page(m, is_note)
        for n in refs(m):
            if is_note(n) and not any(same(r, m) for r in refs(n)):
                msgs.append(f"ONEWAY  <{label(m)}> {mtext!r} "
                            f"(p{mpage or '?'}) -> note")

    allmc = []
    for k in as_list(root.get("/K")):
        if is_elem(k):
            allmc.extend(c for c in contents(k, None, lambda e: False)
                         if isinstance(c, tuple))
    seen, dups = set(), []
    for c in allmc:
        if c in seen and c not in dups:
            dups.append(c)
        seen.add(c)

    def mclist(items):
        shown = ", ".join(f"p{pageno.get(p, '?')} MCID {m}"
                          for p, m in items[:10])
        return shown + (f" (and {len(items) - 10} more)"
                        if len(items) > 10 else "")

    if dups:
        msgs.append(f"DUPMC   {len(dups)} marked content(s): {mclist(dups)}")
    orphans = sorted((c for c in texts if c not in seen),
                     key=lambda c: (pageno.get(c[0], 0), c[1]))
    if orphans:
        msgs.append(f"ORPHMC  {len(orphans)} marked content(s): "
                    f"{mclist(orphans)}")
    for pg, n in untagged_text(pdf):
        msgs.append(f"UNTAGGED p{pg}: {n} text operator(s) outside "
                    f"marked content")

    out = (lines if listing else []) + msgs
    out.append(f"COUNT   {len(notes)} note(s), {len(marks)} mark(s), "
               f"{nlinks} link(s) inside marks")
    return out


def main(argv):
    paths = [a for a in argv if not a.startswith("--")]
    if not paths:
        print(__doc__)
        return 2
    status = 0
    for p in paths:
        print(f"=== {p}")
        for m in check(p, "--list" in argv):
            print("  " + m)
            if not m.startswith(("NOTE ", "MCKID ", "COUNT ")):
                status = 1
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
