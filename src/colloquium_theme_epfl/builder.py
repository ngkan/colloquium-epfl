"""Build branded, self-contained HTML with the pinned Colloquium engine."""

from __future__ import annotations

import base64
import html
import mimetypes
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml

from colloquium.build import build_deck
from colloquium.elements.box import _quote_simple_scalars, process as render_box
from colloquium.md import create_base_md
from colloquium.parse import parse_file
from mdit_py_plugins.dollarmath import dollarmath_plugin

PACKAGE = Path(__file__).resolve().parent
SECTION = re.compile(r'(<section\b[^>]*class="[^"]*\bslide\b[^"]*"[^>]*>)(.*?)</section>', re.DOTALL)
REMOTE_RESOURCE = re.compile(
    r'<script\b[^>]*\bsrc="(?:https?:)?//[^"<>]+"[^>]*>\s*</script>'
    r'|<link\b[^>]*\bhref="(?:https?:)?//[^"<>]+"[^>]*>',
    re.IGNORECASE,
)
TERMINAL_QED = re.compile(r"(?:\s|\\(?:quad|qquad|enspace|thinspace)\b|\\[,;! ])*\\square\s*$")


def _proof_body(md, source: str) -> str:
    """Align an authored terminal math square without changing other symbols."""
    tokens = md.parse(source)
    start = None
    display = False
    if tokens and tokens[-1].type == "math_block":
        target = tokens[-1]
        start, display = len(tokens) - 1, True
    elif (len(tokens) >= 3 and tokens[-3].type == "paragraph_open"
          and tokens[-2].type == "inline" and tokens[-1].type == "paragraph_close"):
        children = tokens[-2].children or []
        while children and children[-1].type == "text" and not children[-1].content.strip():
            children.pop()
        if not children or children[-1].type != "math_inline":
            return md.renderer.render(tokens, md.options, {})
        target = children[-1]
        start = len(tokens) - 3
    if start is None or not TERMINAL_QED.search(target.content):
        return md.renderer.render(tokens, md.options, {})
    target.content = TERMINAL_QED.sub("", target.content)
    if not target.content.strip():
        if display:
            tokens.pop()
        else:
            children.pop()
    before = md.renderer.render(tokens[:start], md.options, {})
    ending = md.renderer.render(tokens[start:], md.options, {})
    modifier = " epfl-qed-line--math" if display else ""
    return (
        f'{before}<div class="epfl-qed-line{modifier}">{ending}'
        '<span class="epfl-qed" role="img" aria-label="End of proof"></span></div>\n'
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


def _render_box(spec: dict) -> str:
    """Add math support, then let the native box renderer own its markup."""
    spec = dict(spec)
    md = create_base_md()
    dollarmath_plugin(md, double_inline=True)
    title = str(spec.get("title", "")).strip()
    body = spec.get("content", "")
    if isinstance(body, str):
        spec["content"] = (
            _proof_body(md, body) if title.casefold() == "proof"
            else md.render(body)
        )
    spec["title"] = md.renderInline(title)
    # The native processor receives escaped YAML from rendered code fences.
    return render_box(html.escape(yaml.safe_dump(spec, allow_unicode=True))) + "\n\n"


def _native_box(source: str) -> str:
    try:
        spec = yaml.safe_load(source)
    except yaml.YAMLError:
        # Match the pinned native renderer's tolerance for unquoted colons.
        try:
            spec = yaml.safe_load(_quote_simple_scalars(source))
        except yaml.YAMLError:
            return render_box(html.escape(source)) + "\n\n"
    if not isinstance(spec, dict):
        return render_box(html.escape(source)) + "\n\n"
    return _render_box(spec)


def _expand_boxes(text: str) -> str:
    """Render top-level native box fences, leaving all other Markdown intact."""
    lines = text.splitlines(keepends=True)
    chunks = []
    cursor = 0
    for token in create_base_md().parse(text):
        if (token.type != "fence" or token.level != 0
                or token.info.strip() != "box" or not token.map):
            continue
        start, end = token.map
        chunks.append("".join(lines[cursor:start]))
        chunks.append(_native_box(token.content))
        cursor = end
    chunks.append("".join(lines[cursor:]))
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
    # Keep explicit engine font settings; supply an offline local stack otherwise.
    font_defaults = "\n".join(
        f'--colloquium-font-{role}: "Suisse Int\'l", "Suisse Intl", "Suisse International", Arial, sans-serif;'
        for role in ("heading", "body")
        if not (deck.fonts or {}).get(role)
    )
    if deck.footer is None:
        deck.footer = {"left": "", "center": "", "right": "auto"}
    for slide in deck.slides:
        slide.content = _expand_boxes(slide.content)
    deck.custom_css = (
        f":root {{\n{font_defaults}\n}}\n"
        + (PACKAGE / "theme" / "epfl.css").read_text(encoding="utf-8")
        + "\n" + deck.custom_css
    )
    document = build_deck(deck)
    if re.search(r"<(?:iframe|canvas)\b", document, re.IGNORECASE):
        raise ValueError("Offline EPFL decks use SVG/images instead of Chart.js canvases or iframes")
    logo = _data_url(PACKAGE / "theme" / "assets" / "epfl-logo.svg")
    presentation_title = html.escape(deck.title)

    def brand_slide(match):
        opener, contents = match.groups()
        # Explicit footer.center wins; otherwise use the presentation title.
        contents = contents.replace(
            '<div class="colloquium-footer-center"></div>',
            f'<div class="colloquium-footer-center">{presentation_title}</div>',
        )
        if re.search(r'\bslide--title(?:-left|-sidebar|-banner)?(?=["\s])', opener):
            # The pinned engine appends the footer last within each slide.
            contents = contents.rsplit('<div class="colloquium-footer">', 1)[0]
            contents = f'<header class="epfl-header"><img src="{logo}" alt="EPFL"></header>{contents}'
        else:
            contents = contents.replace(
                '<div class="colloquium-footer-left">',
                f'<div class="colloquium-footer-left"><img class="epfl-footer-logo" src="{logo}" alt="EPFL">',
                1,
            )
        return f"{opener}{contents}</section>"

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
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    return output
