# Authoring mathematical talks

## Start with a plain slide

```markdown
## State the main idea

A short explanation with inline math $x\in\mathbb R^d$.

$$ f(x)=\frac12\|Ax-b\|_2^2. $$
```

Separate slides with `---`. Use `#` for a cover and `##` for content. A cover
uses `<!-- layout: title-left -->`; the theme also restyles Colloquium's other
title layouts with the same left-aligned cover treatment. Author, affiliation,
and date are written explicitly in the cover body, as in `examples/starter.md`.

## Label mathematical statements

```markdown
> [!THEOREM] Theorem 1 · Sufficient decrease
>
> If $f$ has an $L$-Lipschitz gradient, then
>
> $$ f(x-\eta\nabla f(x))\le f(x)-\frac\eta2\|\nabla f(x)\|_2^2. $$
```

Supported markers: `DEFINITION`, `THEOREM`, `LEMMA`, `PROPOSITION`, `ASSUMPTION`,
`REMARK`, and `PROOF`. The text after the marker becomes the label. If omitted,
the label defaults to the kind (for example, "Theorem"). Supply numbers or named
attributions explicitly. Blank quoted lines separate paragraphs and equations.
Do not nest these callouts. Ordinary blockquotes remain ordinary blockquotes.

Theorems and propositions receive a dark red accent; definitions, lemmas, and
assumptions use a neutral accent. Remarks have an open background. Proofs have
an open layout, leaving room for reasoning. Use words as well as colour to
identify the kind of statement.

## Show a derivation

```markdown
> [!PROOF] Proof
>
> $$
> \begin{aligned}
> f(x-\eta g)&\le f(x)-\eta\|g\|_2^2+\frac{L\eta^2}{2}\|g\|_2^2 \\
> &\le f(x)-\frac\eta2\|g\|_2^2.
> \end{aligned}
> $$

<!-- step -->

The final inequality uses $L\eta\le1$. $\square$
```

Slides are static unless you add a reveal marker. Keep a derivation visible
while revealing its explanation. Print/PDF shows every reveal. KaTeX supports
a substantial subset of LaTeX mathematics; see its supported-functions list.
The build embeds the runtime and fonts; it does not require network access when
presenting. Code fences remain literal code and receive basic theme styling.

Inside raw HTML captions or takeaways, use `<span class="math inline">x^2</span>`
for mathematics. Dollar delimiters are parsed in Markdown, not inside raw HTML.

## Put a diagram beside an equation

```markdown
<!-- columns: 45/55 -->

## Connect the formula to the geometry

Your explanation and equations.

|||

<img class="epfl-diagram" src="assets/figure.svg" alt="Describe the mathematical relationship shown.">

<p class="epfl-caption">A short explanatory caption.</p>
```

Use editable SVG for crisp mathematical diagrams. Avoid embedding external
resources inside an SVG. Diagram colours may use EPFL teal `#007480` as a second
series colour, supported by labelled lines or different dash styles.

## Sections, footers, and sources

```markdown
<!-- layout: section-break -->

## Geometry of convex functions

From first-order inequalities to descent.
```

Section dividers stay white and left-aligned. The footer inherits the latest
section title when `footer.left` is empty. An explicit `footer.left` overrides
that behaviour. The right footer defaults to the slide counter. The cover also
counts as a slide.

For a short source line:

```html
<p class="epfl-source">Author (year), Title, Theorem 2.</p>
```

Colloquium's `.bib` support and `[@key]` citation syntax are also available.
Allow space above the footer for sources; bibliography expansion can add slides.

## Customization

The CSS lives in `src/colloquium_theme_epfl/theme/epfl.css`. Consumer decks can
override theme variables or styles in frontmatter:

```yaml
custom_css: |
  :root { --colloquium-font-body: "Suisse Int'l", Arial, sans-serif; }
  .slide .epfl-block { background: #fff; }
```

Suisse Int'l must be installed locally or supplied by its license holder. Arial
is the default, with Helvetica/sans-serif fallbacks. Math uses bundled KaTeX
fonts. At the reference canvas, the theme uses 38 px headings, 28 px body text,
21 px block labels, and 16 px footers. It does not automatically shrink equations.

Keep 64 px horizontal margins. Normal slides reserve roughly 460 px of vertical
body space, reduced when the heading wraps. Prefer another slide over smaller
text. Verify long headings, matrices, fractions, and long equations in both the
browser and PDF.
