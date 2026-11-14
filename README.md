# footnotehyper

[`footnotehyper`](https://ctan.org/pkg/footnotehyper) LaTeX package
development repo and issue tracker.

**MAKE SURE YOUR BUG REPORT PINGS ME (`@jfbu`) ELSE I WILL NOT BE AWARE OF IT**.

## PDF Tagging

`footnotehyper 2.0 2026/11/12` was the first release compatible with the LaTeX
`\DocumentMetadata` command, for documents being tagged or not.

The testing infrastructure (`./dotaggingtests.sh all`) is based upon the one
originally developed in 2024-2025 by the author for the
[jfbu/etoc](https://github.com/jfbu/etoc) project, which was later (in
November 2026) enriched with Python scripts (requiring
[pikepdf](https://pypi.org/project/pikepdf/)) checking the PDF structures.
Those were provided by AI assistance.

## License

<pre>
%     This Work may be distributed and/or modified under the
%     conditions of the LaTeX Project Public License, in its
%     version 1.3c. This version of this license is in
%          http://www.latex-project.org/lppl/lppl-1-3c.txt
%     and the latest version of this license is in
%          http://www.latex-project.org/lppl.txt
%     and version 1.3 or later is part of all distributions of
%     LaTeX version 2005/12/01 or later.
</pre>
