<!-- -->

    Source:  footnotehyper.dtx (2.0 2026/11/12)
    Author:  Jean-François B.
    Info:    hyperref aware footnote.sty
    License: LPPL 1.3c
    Copyright (C) 2016-2021, 2025, 2026 Jean-François B.
                                        <jfbu on github>.

ABSTRACT
========

The `footnotehyper` package gathers footnotes (`\begin{savenotes}`) and
delivers them later (at `\end{savenotes}`), even if the intervening
material consists, for example, of tabulars, minipages or framed
contents. It also provides a `footnote` environment whose contents may
include verbatim material.

It is a successor to the long obsolete `footnote` package by Mark Wooding
(`1.13 1997/01/28`). Originally (`0.9c 2016/04/19`) `footnotehyper`
patched that package for `hyperref` compatibility and fixed some of its
bugs, among them its incompatibility with `color/xcolor` and with
`babel-french`, and the failure of its `footnote` environment when used
with an optional argument `[NUM]`.

Since `0.99 2017/02/16` all macros are defined internally and the
`footnote` package is not loaded at all. Its user interface is kept,
hence the two packages cannot be used together.

Since `1.0 2017/03/07` `footnotehyper` can also be used in the absence
of `hyperref`, or when the latter is loaded with its
`hyperfootnotes=false` option. The order in which `footnotehyper` and
`hyperref` are loaded is inconsequential.

Since `2.0 2026/11/12` tagging is supported (tested with pdfLaTeX and
LuaLaTeX). The LaTeX release 2026-11-01 or later is required.

INSTALLATION
============

The recommended way is to first extract the package (.sty)
and driver (.tex) files from footnotehyper.dtx via

    etex footnotehyper.dtx

and then produce the documentation via

    latex footnotehyper.tex (twice)
    dvipdfmx footnotehyper.dvi

It is also possible to produce simultaneously the package
and the documentation via one of these two routes:

    pdflatex footnotehyper.dtx (twice)

or

    latex footnotehyper.dtx (twice)
    dvips
    ps2pdf

The method using the extracted file footnotehyper.tex produces
the smallest pdf file and is the officially preferred one as
it allows to set options in footnotehyper.tex to customize the
footnotehyper.pdf file:

- scrartcl class options (paper size, font size, ...)
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

- Jean-François B. `<jfbu on github>`

This Work consists of the main source file footnotehyper.dtx
and the derived files footnotehyper.sty, footnotehyper.tex,
footnotehyper.pdf, footnotehyper.dvi.
