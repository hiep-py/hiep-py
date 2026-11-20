"""Builds the animated SVGs of the profile README (dark and light). Run: python3 assets/make.py

GitHub shows README pictures as <img>: CSS animations inside an SVG play, external fonts and scripts do not, so
everything uses system fonts and pure CSS.
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent

THEMES = {
    "dark": {
        "bg1": "#050505", "bg2": "#0f2a22", "ink": "#f5f2ec", "muted": "#9aa39e", "line": "#1f2a26",
        "accent": "#3ddc97", "accent2": "#7de8c4", "pill": "#0f1714", "pillLine": "#24332d",
    },
    "light": {
        "bg1": "#fffdf8", "bg2": "#e8f1ec", "ink": "#171613", "muted": "#5f6560", "line": "#ddd8cf",
        "accent": "#1f5a47", "accent2": "#2c7a60", "pill": "#ffffff", "pillLine": "#d6dcd8",
    },
}

SANS = "-apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"

# Typed one after another in the header, then erased.
LINES = [
    "AI integration & automation",
    "building ASC - scam checker for Vietnam",
    "building TRAM - offline book reader",
    "clean systems, fast and stable",
]


def header(t: dict) -> str:
    """A black-and-white poster: giant LACDEV drawn as an outline then filled, a ticker running along the bottom."""
    w, h = 1200, 380
    ink, paper = t["ink"], t["bg1"]
    ticker = "AI INTEGRATION  /  AUTOMATION  /  SYSTEM DESIGN  /  PERFORMANCE  /  ANDROID  /  WEB  /  LINUX  /  "
    tw = 1500  # forced width of one ticker copy (textLength), so the loop is seamless with any font
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hồ Hiệp · LacDev">
  <style>
    .meta {{ font: 700 14px {MONO}; fill: {ink}; letter-spacing: 2px; }}
    .dim {{ fill-opacity: .55; }}
    .big {{ font: 900 220px 'Arial Black', 'Helvetica Neue', Arial, sans-serif; fill: {ink}; fill-opacity: 0; stroke: {ink}; stroke-width: 2;
            stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: draw 2.4s .2s cubic-bezier(.6,0,.2,1) forwards, fill .8s 2.3s ease forwards; }}
    .rule {{ stroke: {ink}; stroke-width: 1; }}
    .band {{ fill: {ink}; }}
    .tick {{ font: 700 15px {MONO}; fill: {paper}; letter-spacing: 3px; }}
    .run {{ animation: run 28s linear infinite; }}
    .blink {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fill {{ to {{ fill-opacity: 1; stroke-width: 0; }} }}
    @keyframes run {{ to {{ transform: translateX(-{tw}px); }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .big {{ animation: none; fill-opacity: 1; stroke-width: 0; }} .run, .blink {{ animation: none; }} }}
  </style>
  <rect width="{w}" height="{h}" fill="{paper}"/>
  <text x="40" y="52" class="meta">HỒ HIỆP</text>
  <text x="600" y="52" class="meta dim" text-anchor="middle">DEVELOPER — VIETNAM</text>
  <text x="1160" y="52" class="meta" text-anchor="end">LACDEV.XYZ</text>
  <line x1="40" y1="72" x2="1160" y2="72" class="rule"/>
  <text x="34" y="272" class="big" textLength="1132" lengthAdjust="spacingAndGlyphs">LACDEV</text>
  <text x="40" y="306" class="meta dim" textLength="330" lengthAdjust="spacing">~/hiep $ build --clean --fast --stable</text>
  <rect x="378" y="294" width="10" height="16" class="band blink"/>
  <rect x="0" y="{h - 46}" width="{w}" height="46" class="band"/>
  <g class="run">
    <text x="0" y="{h - 18}" class="tick" textLength="{tw}" lengthAdjust="spacing">{ticker}</text>
    <text x="{tw}" y="{h - 18}" class="tick" textLength="{tw}" lengthAdjust="spacing">{ticker}</text>
  </g>
</svg>
"""


STACK = [
    ("Ngôn ngữ", ["Python", "TypeScript", "JavaScript", "Kotlin", "C#/C++", "Rust"]),
    ("Web & app", ["React", "Node.js", "Bun", "Jetpack Compose", "Tailwind"]),
    ("Hạ tầng", ["Linux", "Docker", "MongoDB", "Cloudflare", "CI/CD", "Git"]),
    ("AI", ["LLM integration", "On-device ML", "ONNX Runtime", "OCR", "Automation bots"]),
]


def stack(t: dict) -> str:
    w = 1200
    row_h = 72
    h = 24 + row_h * len(STACK)
    char_w = 9.9  # 17px sans, average
    parts = []
    n = 0
    for r, (label, items) in enumerate(STACK):
        y = 24 + r * row_h
        parts.append(f'<text x="0" y="{y + 29}" class="lab">{escape(label)}</text>')
        x = 190
        for item in items:
            pw = len(item) * char_w + 30
            delay = 0.08 * n
            parts.append(
                f'<g class="pill" style="animation-delay:{delay:.2f}s">'
                f'<rect x="{x}" y="{y}" width="{pw:.0f}" height="46" rx="23"/>'
                f'<text x="{x + pw / 2:.0f}" y="{y + 29}" text-anchor="middle">{escape(item)}</text></g>'
            )
            x += pw + 12
            n += 1
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Công nghệ">
  <style>
    .lab {{ font: 700 16px {MONO}; fill: {t['muted']}; letter-spacing: 1.5px; text-transform: uppercase; }}
    .pill rect {{ fill: {t['pill']}; stroke: {t['pillLine']}; }}
    .pill text {{ font: 600 17px {SANS}; fill: {t['ink']}; }}
    .pill {{ animation: pop .6s cubic-bezier(.2,.8,.2,1) both; }}
    .pill:hover rect {{ stroke: {t['accent']}; }}
    @keyframes pop {{ from {{ opacity: 0; transform: translateY(8px); }} to {{ opacity: 1; transform: none; }} }}
    @media (prefers-reduced-motion: reduce) {{ .pill {{ animation: none; }} }}
  </style>
  {''.join(parts)}
</svg>
"""


for name, theme in THEMES.items():
    (OUT / f"header-{name}.svg").write_text(header(theme), encoding="utf-8")
    (OUT / f"stack-{name}.svg").write_text(stack(theme), encoding="utf-8")
print("ok")
