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
        result = self.build("# Talk\n\n---\n\n## Result\n\n$$ x^2+y^2=1 $$\n")
        self.assertNotRegex(result, r'<(?:script|link)[^>]+(?:src|href)="https?://')
        self.assertNotRegex(result, r'url\(["\']?(?:https?://|fonts/)')
        self.assertIn("data:font/woff2;base64,", result)
        self.assertIn("katex", result)
        self.assertEqual(result.count('class="epfl-header"'), 2)

    def test_local_images_resolve_relative_to_source_and_survive_relocation(self):
        (self.root / "figure.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
        result = self.build("## Figure\n\n![Diagram](figure.svg)\n")
        self.assertRegex(result, r'<img src="data:image/svg\+xml;base64,')

    def test_callouts_keep_math_and_manual_labels_and_plain_quotes(self):
        result = self.build(
            "## Result\n\n> [!THEOREM] Theorem 7 · A bound\n>\n> $x\\le y$.\n\n"
            "> An ordinary quote.\n"
        )
        self.assertIn('class="epfl-block epfl-theorem"', result)
        self.assertIn("Theorem 7 · A bound", result)
        self.assertIn('class="math inline"', result)
        self.assertIn("<blockquote>\n<p>An ordinary quote.</p>", result)

    def test_section_footer_inherits_but_explicit_footer_wins(self):
        body = "<!-- layout: section-break -->\n\n## Geometry\n\n---\n\n## Result\n\nText."
        result = self.build(body)
        self.assertEqual(result.count('class="colloquium-footer-left">Geometry'), 2)
        result = self.build("---\nfooter:\n  left: Seminar\n---\n\n" + body)
        self.assertEqual(result.count('class="colloquium-footer-left">Seminar'), 2)

    def test_remote_images_and_wrong_aspect_ratio_fail_clearly(self):
        with self.assertRaisesRegex(ValueError, "Download remote images"):
            self.build("## Figure\n\n![Diagram](https://example.org/figure.png)")
        with self.assertRaisesRegex(ValueError, "16:9"):
            self.build("---\naspect_ratio: '4:3'\n---\n\n## Result")

    def test_multiline_math_in_callouts_has_no_quote_markers(self):
        result = self.build(
            "## Proof\n\n> [!PROOF] Proof\n>\n> $$\n"
            "> \\begin{aligned}\n> a&=b\n> \\end{aligned}\n> $$\n"
        )
        self.assertNotIn("&gt; \\begin{aligned}", result)
        self.assertIn("\\begin{aligned}\na&amp;=b", result)

    def test_callout_markers_in_code_fences_are_not_transformed(self):
        result = self.build("## Syntax\n\n```markdown\n> [!THEOREM] Label\n> Content.\n```\n")
        self.assertNotIn('class="epfl-block epfl-theorem"', result)
        self.assertIn("[!THEOREM] Label", result)

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


if __name__ == "__main__":
    unittest.main()
