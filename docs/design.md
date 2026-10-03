# Design specification

Approved direction: minimal academic; balanced mathematical density; reusable
theme in a standalone repository with a separate mathematical showcase.

| Element | Specification |
| --- | --- |
| Canvas | 16:9, 1280 × 720 reference size, white |
| Header | Small EPFL logo above a left-aligned charcoal heading |
| Rule | 2 px EPFL Swiss red beneath the heading |
| Text | Arial; 28 px body, 38 px headings, conventional serif math |
| Cover | 62 px title, subtitle, author/affiliation/date area |
| Margins | 64 px horizontally; reserved header and footer zones |
| Statements | Upright prose; bold labels; optional author-supplied names/numbers |
| Blocks | Subtle neutral surface and narrow accent, square corners |
| Proofs | Open layout, normally 3–5 aligned derivation lines |
| Footer | Section label and page counter, 16 px muted text |
| Reveals | Static default; author-controlled optional steps |
| Outputs | Offline HTML and vector PDF via Chromium |

The outstanding planning choices were resolved using the proposed defaults when
implementation was requested: upright theorem statements, author-supplied
numbering, and convex analysis/probability examples.

The dark red `#B51F1F` supplies readable emphasis and labels. Bright red `#FF0000`
is used for the logo and thin rules. Charcoal is `#413D3A`; neutral border colour
is `#CAC7C7`. The geometry example uses EPFL teal `#007480` for a second labelled
line. No full-width filled title bar is used.

References:

- [EPFL public brand guidelines](https://www.epfl.ch/about/overview/wp-content/uploads/2020/06/EPFL-brand-guidelines.pdf): logo position, palette, white space, Suisse Int'l, Arial alternative.
- [EPFL Visual Communication](https://www.epfl.ch/campus/services/communication/en/visual-communication/): official presentation examples and restricted template downloads.
- [Auriga](https://github.com/anishathalye/auriga): minimal academic styling.
- [Moloch](https://moloch.ink/): restrained presentation structure and emphasis on content space.
- [Unofficial EPFL Beamer template](https://github.com/jupall/EPFLtemplate): institutional comparison.

These are design references; their theme source code is not incorporated.
