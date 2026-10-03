# Initial verification

Verified on 3 October 2026 with Python 3.13.5, Colloquium 0.2.3 at the pinned
revision, KaTeX 0.18.10, and Google Chrome 154 on macOS.

- The standalone locked environment installs and runs independently of `aitalk`.
- `make test` checks image paths, self-contained math/fonts, branding, callouts,
  multiline quoted math, literal code examples, section footers, and clear input
  failures.
- `make build`, `make starter`, and `make export` produce the documented outputs.
- A temporary headless Chrome review blocks all HTTP/HTTPS resource requests.
  The showcase makes zero external resource requests and reports zero page errors
  or KaTeX errors; all eight slides render.
- Element bounds were checked against the content margins, column boundaries,
  source lines, and footer zones. The final showcase reports no overflow.
- Keyboard navigation keeps the proof takeaway hidden on entry, reveals it on
  the next advance, and then advances to the geometry slide.
- The exported PDF has eight 16:9 pages, 960 × 540 points. Every page was rendered
  with Poppler and visually inspected after the final layout changes.
- The source distribution and wheel build successfully and include theme CSS,
  the SVG logo, the KaTeX runtime/stylesheet/license, and all WOFF2 math fonts.

The browser review initially exposed two footer collisions and a pinned-engine
multiline quote/math parsing issue. Diagram height and the probability layout
were adjusted. Theme callouts now remove their quote prefixes before rendering
their content, preserving aligned mathematics without stray greater-than signs.

This checks the included examples, not arbitrary future decks. Recheck layout
when authoring new content. Arial falls back to Helvetica or the platform's
sans-serif if unavailable. External reference links need internet access when
followed; presentation resources are embedded.
