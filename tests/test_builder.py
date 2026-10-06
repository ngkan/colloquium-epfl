"""Integration contracts for distribution, source paths, and offline math."""

import tempfile
import unittest
from pathlib import Path

from colloquium_theme_epfl import build_epfl


class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def build(self, text):
        source = self.root / "talk.md"
        source.write_text(text, encoding="utf-8")
        return build_epfl(source, self.root / "elsewhere" / "talk.html").read_text()

    def test_portable_math_deck_has_no_remote_runtime_or_font_sources(self):
        result = self.build("<!-- layout: title-left -->\n\n# Talk\n\n---\n\n## Result\n\n$$ x^2+y^2=1 $$\n")
        self.assertNotRegex(result, r'<(?:script|link)[^>]+(?:src|href)="https?://')
        self.assertNotRegex(result, r'url\(["\']?(?:https?://|fonts/)')
        self.assertIn("data:font/woff2;base64,", result)
        self.assertIn("katex", result)
        self.assertEqual(result.count('class="epfl-header"'), 1)
        self.assertEqual(result.count('<div class="colloquium-footer">'), 1)
        self.assertEqual(result.count('<div class="colloquium-footer-left"><img class="epfl-footer-logo"'), 1)

    def test_local_images_resolve_relative_to_source_and_survive_relocation(self):
        (self.root / "figure.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        result = self.build("## Figure\n\n![Diagram](figure.svg)\n")
        self.assertRegex(result, r'<img src="data:image/svg\+xml;base64,')

    def test_native_boxes_keep_math_and_manual_labels_and_plain_quotes(self):
        result = self.build(
            "## Result\n\n```box\ntitle: Theorem 7 [A bound]\ntone: blue\n"
            "content: |\n  $x\\le y$.\n```\n\n"
            "> An ordinary quote.\n"
        )
        self.assertIn('class="colloquium-box colloquium-box--blue"', result)
        self.assertIn("Theorem 7 [A bound]", result)
        self.assertIn('class="math inline"', result)
        self.assertIn("<blockquote>\n<p>An ordinary quote.</p>", result)

    def test_presentation_footer_persists_across_sections_but_explicit_footer_wins(self):
        body = "<!-- layout: section-break -->\n\n## Geometry\n\n---\n\n## Result\n\nText."
        metadata = "---\ntitle: Convexity & concentration\n---\n\n"
        result = self.build(metadata + body)
        self.assertEqual(result.count('class="colloquium-footer-center">Convexity &amp; concentration'), 2)
        result = self.build("---\ntitle: Convexity & concentration\nfooter:\n  center: Seminar\n  right: auto\n---\n\n" + body)
        self.assertEqual(result.count('class="colloquium-footer-center">Seminar'), 2)
        result = self.build(metadata + body + "\n\n---\n\n<!-- layout: section-break -->\n\n## Descent")
        self.assertEqual(result.count('class="slide slide--section-break'), 2)
        self.assertNotIn('class="epfl-section-number"', result)
        self.assertEqual(result.count('class="colloquium-footer-center">Convexity &amp; concentration'), 3)

    def test_remote_images_and_wrong_aspect_ratio_fail_clearly(self):
        with self.assertRaisesRegex(ValueError, "Download remote images"):
            self.build("## Figure\n\n![Diagram](https://example.org/figure.png)")
        with self.assertRaisesRegex(ValueError, "16:9"):
            self.build("---\naspect_ratio: '4:3'\n---\n\n## Result")

    def test_multiline_math_in_native_boxes(self):
        result = self.build(
            "## Proof\n\n```box\ntitle: Proof\ncontent: |\n  $$\n"
            "  \\begin{aligned}\n  a&=b\n  \\end{aligned}\n  $$\n```\n"
        )
        self.assertNotIn("&gt; \\begin{aligned}", result)
        self.assertIn("\\begin{aligned}\na&amp;=b", result)

    def test_old_callout_markers_are_ordinary_blockquotes(self):
        result = self.build("## Result\n\n> [!THEOREM]\n> A statement.\n")
        result = result[result.index('<section '):]
        self.assertNotIn('<div class="colloquium-box ', result)
        self.assertIn('<blockquote>', result)
        self.assertIn('[!THEOREM]', result)

    def test_terminal_proof_square_aligns_without_removing_mathematical_squares(self):
        for ending in (r"Done. $\square$", r"$$ x=y.\quad\square $$",
                       r"Thus $x=y.\quad\square$", r"$$ \square $$"):
            with self.subTest(ending=ending):
                result = self.build("## Proof\n\n```box\ntitle: Proof\ncontent: |\n  " + ending + "\n```\n")
                self.assertEqual(result.count('class="epfl-qed"'), 1)
                self.assertIn('aria-label="End of proof"', result)
                self.assertNotIn('\\square', result[result.index('<section '):])
        for kind, ending in (("THEOREM", r"$\square$"),
                             ("PROOF", r"The operator $\square$ acts on $f$."),
                             ("PROOF", r"`$\square$`"),
                             ("PROOF", "The proof continues.")):
            with self.subTest(kind=kind, ending=ending):
                result = self.build(f"## Result\n\n```box\ntitle: {kind.capitalize()}\ncontent: |\n  {ending}\n```\n")
                self.assertNotIn('class="epfl-qed"', result)

    def test_native_boxes_keep_math_markdown_options_and_qed(self):
        result = self.build(r'''## Result

```box
title: Proof
tone: purple
align: right
size: 0.9
compact: true
content: |
  Use $x_1<y_1$ and **a bound**.

  - First step.
  - Second step with [a link](https://example.org).

  $$
  \begin{aligned}
  x_1&<y_1\\
  y_1&=z_1
  \end{aligned}\quad\square
  $$
```
''')
        result = result[result.index('<section '):]
        self.assertIn('colloquium-box--purple colloquium-box--align-right colloquium-box--compact', result)
        self.assertIn('style="font-size: 0.9em"', result)
        self.assertIn('<div class="colloquium-box-title">Proof</div>', result)
        self.assertIn('<span class="math inline">x_1&lt;y_1</span>', result)
        self.assertIn('<strong>a bound</strong>', result)
        self.assertIn('<ul>', result)
        self.assertIn('href="https://example.org"', result)
        self.assertIn('class="math block"', result)
        self.assertEqual(result.count('class="epfl-qed"'), 1)
        self.assertNotIn('language-box', result)

    def test_native_boxes_preserve_validation_and_colon_tolerance(self):
        for source, expected in (
            ('title: Result: a bound\ncontent: |\n  $x_1<y_1$\n',
             '<span class="math inline">x_1&lt;y_1</span>'),
            ('- invalid\n', 'Box spec must be a YAML mapping'),
            ('title: [unterminated\n', 'Invalid box YAML'),
            ('{}\n', 'Box requires title or content'),
        ):
            with self.subTest(source=source):
                result = self.build('## Result\n\n```box\n' + source + '```\n')
                self.assertIn(expected, result)

    def test_native_box_examples_in_outer_fences_remain_literal(self):
        result = self.build('## Syntax\n\n````markdown\n```box\ntitle: Proof\n'
                            'content: |\n  Example.\n```\n````\n')
        result = result[result.index('<section '):]
        self.assertNotIn('<div class="colloquium-box ', result)
        self.assertIn('```box', result)

    def test_single_quoted_local_image_is_embedded(self):
        (self.root / "figure.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        result = self.build("## Figure\n\n<img src='figure.svg' alt='Diagram'>")
        self.assertIn("src='data:image/svg+xml;base64,", result)

    def test_source_cannot_be_overwritten(self):
        source = self.root / "talk.md"
        source.write_text("## Result\n\nKeep me.")
        with self.assertRaisesRegex(ValueError, "overwrite"):
            build_epfl(source, source)
        self.assertIn("Keep me.", source.read_text())

    def test_native_markdown_figures_footnotes_and_reveals(self):
        (self.root / "figure.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        result = self.build(
            "---\nfigure_captions: true\n---\n\n"
            "<!-- columns: 45/55 -->\n\n## Geometry\n\nAn explanation.\n\n|||\n\n"
            "![A parabola.](figure.svg)\n\n"
            "<!-- footnote: A source with $x^2$. -->\n\n"
            "---\n\n## Result\n\n<!-- size: small -->\n\n"
            "1. A reference with a [link](https://example.org).\n\n"
            "<!-- step -->\n\nThe condition is $L\\eta \\le 1$.\n"
        )
        self.assertFalse('window.colloquiumFitDisplayMathIn = function() {};' in result)
        result = result[result.index('<section '):result.rindex('</section>') + len('</section>')]
        self.assertIn('<figure class="colloquium-figure">', result)
        self.assertIn('<figcaption class="colloquium-figure-caption">A parabola.</figcaption>', result)
        self.assertIn('class="colloquium-slide-footnote"', result)
        self.assertIn('class="slide slide--content size-small"', result)
        self.assertIn('<ol>', result)
        self.assertRegex(result, r'class="fragment" data-fragment-index="1"><p>')
        self.assertIn('A source with <span class="math inline">x^2</span>', result)

    def test_examples_need_no_raw_html(self):
        examples = Path(__file__).resolve().parents[1] / "examples"
        for source in examples.glob("*.md"):
            with self.subTest(source=source.name):
                self.assertNotRegex(source.read_text(), r'</?[A-Za-z][^>]*>')


if __name__ == "__main__":
    unittest.main()
