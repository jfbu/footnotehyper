<!-- -->

    Source:  footnotehyper.dtx (v0.9f 2016/10/03)
    Author:  Jean-Francois B.
    Info:    hyperref aware footnote.sty
    License: LPPL 1.3c
    Copyright (C) 2016 Jean-Francois B. <jfbu on github>.

ABSTRACT
========

The `footnote` package by Mark Wooding (which dates back to 1997)
allows to gather footnotes (`\savenotes`) and later insert them
(`\spewnotes`) at the bottom of the page, even if the intervening
material consists of tabulars, minipages or framed contents for
example. There is a command to patch any given environment to do
the `\savenotes/\spewnotes` commands automatically. Also there is
a `footnote` environment which allows to insert verbatim material.

The `footnotehyper` package loads `footnote.sty` and rewrites a
number of its commands to add `hyperref` awareness and to fix some
issues, particularly the one of incompatibility with
`color/xcolor`. The incompatibility with `babel-frenchb` is
addressed, too. In case of absence of `hyperref`, `footnotehyper`
limits itself to partially fix some of these issues.

This package provides no facility dedicated to footnotes from
floating environments.

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
