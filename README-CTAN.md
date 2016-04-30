<!-- -->

    Source:  footnotehyper.dtx (v0.9e 2016/04/30)
    Author:  Jean-Francois B.
    Info:    hyperref aware footnote.sty
    License: LPPL 1.3c or later
    Copyright (C) 2016 Jean-Francois B. <jfbu on github>.

ABSTRACT
========

The `footnote` package by Mark Wooding dates back to 1997 and has
not been made `hyperref` compatible. The aim of the present
package is to do that. Its state is what I found sufficiently
well-working on a current LaTeX document of mine.

For those who don't know: the `footnote` package allows via
`\savenotes` to gather footnotes and later release them via
`\spewnotes` (one can also use a `savenotes` environment.)
Thus footnotes emitted from tabulars or minipages
are not separated from the general document stream of footnotes,
and are printed with the others at bottom of page. This works also
for environments like `framed` (1) from the eponymous package and
avoids the `\footnotemark/\footnotetext` approach, which anyhow is
not immediately `hyperref` compatible. The `footnote` package has
a facility to patch any user-chosen environment to do the
`\savenotes/\spewnotes` automatically.

This package provides no facility for handling footnotes from floating
environments.

Some issues from `footnote.sty` made it incompatible with the
`color` and `xcolor` packages; this is corrected by `footnotehyper`. The
compatibility with `babel-frenchb` is improved, too.

The loading of `hyperref` (either before or after) is mandatory
but left to the user.

(1): in case of multi-page content, the footnotes are delivered in
the last page.

INSTALLATION
============

To extract the package (.sty) and driver (.tex) files from
footnotehyper.dtx:

- if footnotehyper.ins is present:   etex footnotehyper.ins
- without footnotehyper.ins:         etex footnotehyper.dtx
- or run latex or pdflatex directly on footnotehyper.dtx

At least three ways to produce footnotehyper.pdf (method (1) is
preferred):

1. latex footnotehyper.tex (twice), then dvipdfmx
2. pdflatex footnotehyper.dtx (twice)
3. latex footnotehyper.dtx (twice), then dvips, then ps2pdf

Method (1) produces the smallest pdf files.
Options can be set in footnotehyper.tex:

- scrdoc class options (paper size, font size, ...)
- with or without source code,
- with dvipdfmx or with latex+dvips or pdflatex.

Installation:

    footnotehyper.sty    -> TDS:tex/latex/footnotehyper/footnotehyper.sty
    footnotehyper.dtx    -> TDS:source/latex/footnotehyper/footnotehyper.dtx
    footnotehyper.pdf    -> TDS:doc/latex/footnotehyper/footnotehyper.pdf
    README.md            -> TDS:doc/latex/footnotehyper/README.md

The other files may be discarded.

LICENSE
=======

This Work may be distributed and/or modified under the conditions
of the LaTeX Project Public License, version 1.3c. This version of
this license is in:

> <http://www.latex-project.org/lppl/lppl-1-3c.txt>

and the latest version of this license is in:

> <http://www.latex-project.org/lppl.txt>

Version 1.3 or later is part of all distributions of
LaTeX version 2005/12/01 or later.

The Author of this Work is:

- Jean-Francois B. `<jfbu on github>`

This Work consists of the main source file footnotehyper.dtx and the
derived files footnotehyper.sty, footnotehyper.ins, footnotehyper.tex,
footnotehyper.pdf, footnotehyper.dvi.
