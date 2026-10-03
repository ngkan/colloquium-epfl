"""Build branded, self-contained HTML using Colloquium's public deck API."""

from __future__ import annotations

import base64
import html
import mimetypes
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from colloquium.build import build_deck
from colloquium.md import create_base_md
from colloquium.parse import parse_file
from mdit_py_plugins.dollarmath import dollarmath_plugin

PACKAGE = Path(__file__).resolve().parent
CALLOUT = re.compile(
    r"^>[ \t]*\[!(DEFINITION|THEOREM|LEMMA|PROPOSITION|ASSUMPTION|REMARK|PROOF)\]"
    r"([^\n]*)(?:\n|$)((?:^>[^\n]*(?:\n|$))*)",
    re.MULTILINE,
)
SECTION = re.compile(r'(<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>)(.*?)</section>', re.DOTALL)
REMOTE_RESOURCE = re.compile(
    r'<script\b[^>]*\bsrc="(?:https?:)?//[^"<>]+"[^>]*>\s*</script>'
    r'|<link\b[^>]*\bhref="(?:https?:)?//[^"<>]+"[^>]*>',
    re.IGNORECASE,
)


def _data_url(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _math_css() -> str:
    katex = PACKAGE / "vendor" / "katex"
    css = (katex / "katex.min.css").read_text(encoding="utf-8")
    # WOFF2 is supported by current browsers; omit unused WOFF/TTF fallbacks.
    css = re.sub(r',url\([^)]*\) format\("(?:woff|truetype)"\)', "", css)
    return re.sub(
        r"url\((fonts/[^)]+\.woff2)\)",
        lambda match: f'url("{_data_url(katex / match.group(1))}")',
        css,
    )


def _callout(match: re.Match) -> str:
    kind, title, body = match.groups()
    md = create_base_md()
    dollarmath_plugin(md, double_inline=True)
    title = md.renderInline(title.strip() or kind.capitalize())
    # Strip quote prefixes before math parsing. The pinned engine otherwise
    # retains quote markers inside multiline $$ blocks (e.g. aligned proofs).
    body = md.render(re.sub(r"^>[ \t]?", "", body, flags=re.MULTILINE))
    return (
        f'<aside class="epfl-block epfl-{kind.lower()}" aria-label="{kind.capitalize()}">'
        f'<p class="epfl-block-title">{title}</p>{body}</aside>\n\n'
    )


def _expand_callouts(text: str) -> str:
    """Leave literal top-level fenced and indented code examples untouched."""
    lines = text.splitlines(keepends=True)
    protected = [
        token.map for token in create_base_md().parse(text)
        if token.type in {"fence", "code_block"} and token.level == 0 and token.map
    ]
    chunks = []
    cursor = 0
    for start, end in protected:
        chunks.append(CALLOUT.sub(_callout, "".join(lines[cursor:start])))
        chunks.append("".join(lines[start:end]))
        cursor = end
    chunks.append(CALLOUT.sub(_callout, "".join(lines[cursor:])))
    return "".join(chunks)


def build_epfl(source: str | Path, output: str | Path | None = None) -> Path:
    """Build a 16:9 deck, embedding its images, math runtime, and math fonts.

    Image paths are relative to the Markdown file. Remote images/iframes and
    Chart.js canvases are rejected rather than producing a partial offline deck.
    """
    source = Path(source).resolve()
    output = Path(output).resolve() if output else source.with_suffix(".html")
    if output == source:
        raise ValueError("HTML output must not overwrite the Markdown source")
    deck = parse_file(str(source))
    if deck.aspect_ratio != "16:9":
        raise ValueError("The EPFL theme currently supports 16:9 slides")
    deck.theme = "default"
    deck.fonts = {"heading": "Arial", "body": "Arial"}
    if deck.footer is None:
        deck.footer = {"left": "", "center": "", "right": "auto"}
    for slide in deck.slides:
        slide.content = _expand_callouts(slide.content)
    deck.custom_css = (PACKAGE / "theme" / "epfl.css").read_text(encoding="utf-8") + "\n" + deck.custom_css
    document = build_deck(deck)
    if re.search(r"<(?:iframe|canvas)\b", document, re.IGNORECASE):
        raise ValueError("Offline EPFL decks use SVG/images instead of Chart.js canvases or iframes")
    logo = _data_url(PACKAGE / "theme" / "assets" / "epfl-logo.svg")
    current_section = ""

    def brand_slide(match):
        nonlocal current_section
        opener, contents = match.groups()
        heading = re.search(r"<h2>(.*?)</h2>", contents, re.DOTALL)
        if "slide--section-break" in opener and heading:
            current_section = heading.group(1)
        # Explicit footer.left wins; otherwise inherit the latest section title.
        contents = contents.replace(
            '<div class="colloquium-footer-left"></div>',
            f'<div class="colloquium-footer-left">{current_section}</div>',
        )
        header = f'<header class="epfl-header"><img src="{logo}" alt="EPFL"></header>'
        return f"{opener}{header}{contents}</section>"

    document = SECTION.sub(brand_slide, document)

    def embed_image(match):
        prefix, quote, original = match.groups()
        original = html.unescape(original)
        if original.startswith("data:"):
            return match.group(0)
        parsed = urlparse(original)
        if parsed.scheme or parsed.netloc:
            raise ValueError(f"Download remote images before building an offline deck: {original}")
        asset = (source.parent / unquote(parsed.path)).resolve()
        return f"{prefix}{quote}{_data_url(asset)}{quote}"

    document = re.sub(r'''(<img\b[^>]*\bsrc=)(["'])(.*?)\2''', embed_image, document)
    document = REMOTE_RESOURCE.sub("", document)
    math_js = (PACKAGE / "vendor" / "katex" / "katex.min.js").read_text(encoding="utf-8")
    document = document.replace(
        "</head>",
        f"<style>{_math_css()}</style>\n<script>{math_js}</script>\n</head>",
        1,
    )
    # Preserve the author's chosen equation size. Layout QA reports overflow.
    # This late assignment runs before Colloquium's load handler renders math.
    document = document.replace(
        "</body>",
        '<script>window.colloquiumFitDisplayMathIn = function() {};</script>\n</body>',
        1,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output
