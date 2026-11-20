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
    w, h = 1200, 320
    cycle = 16  # seconds for all lines
    slot = cycle / len(LINES)
    char_w = 13.2  # monospace 22px
    typed = []
    for i, line in enumerate(LINES):
        width = len(line) * char_w + 4
        a = i / len(LINES)
        b = (i + 1) / len(LINES)
        # Hidden, type in (35% of the slot), hold, erase (15%), hidden.
        k = [0, a, a + 0.35 * (b - a), b - 0.15 * (b - a), b, 1]
        k = [round(x, 4) for x in k]
        typed.append(f"""
    <clipPath id="c{i}"><rect x="96" y="196" height="40" width="0">
      <animate attributeName="width" dur="{cycle}s" repeatCount="indefinite" calcMode="linear"
        keyTimes="{';'.join(map(str, k))}" values="0;0;{width:.0f};{width:.0f};0;0"/>
    </rect></clipPath>
    <text x="96" y="224" class="type" clip-path="url(#c{i})">{escape(line)}</text>""")
    # The caret follows the typed text of each slot.
    caret_values = []
    caret_times = []
    for i, line in enumerate(LINES):
        width = len(line) * char_w + 4
        a = i / len(LINES)
        b = (i + 1) / len(LINES)
        caret_times += [a, a + 0.35 * (b - a), b - 0.15 * (b - a), b - 0.0001 if i < len(LINES) - 1 else 1]
        caret_values += [96, 96 + width, 96 + width, 96]
    caret_times[0] = 0
    caret = (
        f'<rect class="caret" y="203" width="12" height="26" x="96">'
        f'<animate attributeName="x" dur="{cycle}s" repeatCount="indefinite" '
        f'keyTimes="{";".join(str(round(x, 4)) for x in caret_times)}" '
        f'values="{";".join(f"{v:.0f}" for v in caret_values)}"/></rect>'
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hồ Hiệp · LacDev">
  <style>
    .name {{ font: 800 76px {SANS}; fill: {t['ink']}; letter-spacing: -2px; animation: up .9s cubic-bezier(.2,.8,.2,1) both; }}
    .tag {{ font: 700 15px {MONO}; fill: {t['accent']}; letter-spacing: 3px; animation: up .9s .15s cubic-bezier(.2,.8,.2,1) both; }}
    .type {{ font: 500 22px {MONO}; fill: {t['muted']}; }}
    .prompt {{ font: 700 22px {MONO}; fill: {t['accent']}; }}
    .caret {{ fill: {t['accent']}; animation: blink 1s steps(1) infinite; }}
    .grid {{ stroke: {t['line']}; stroke-width: 1; }}
    .orbit {{ fill: none; stroke: {t['accent']}; stroke-opacity: .35; stroke-width: 1.5; stroke-dasharray: 4 10; }}
    .spin {{ transform-origin: 1000px 160px; animation: spin 40s linear infinite; }}
    .spin2 {{ transform-origin: 1000px 160px; animation: spin 26s linear infinite reverse; }}
    .dot {{ fill: {t['accent2']}; }}
    .pulse {{ transform-origin: 1000px 160px; animation: pulse 3.2s ease-in-out infinite; }}
    .scan {{ animation: scan 6s ease-in-out infinite; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    @keyframes pulse {{ 0%,100% {{ transform: scale(1); opacity: .9; }} 50% {{ transform: scale(1.08); opacity: 1; }} }}
    @keyframes scan {{ 0% {{ transform: translateX(-300px); opacity: 0; }} 20% {{ opacity: .5; }} 80% {{ opacity: .5; }} 100% {{ transform: translateX(1300px); opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/>
    </linearGradient>
    <pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M40 0H0V40" class="grid" fill="none"/>
    </pattern>
    <linearGradient id="beam" x1="0" x2="1">
      <stop offset="0" stop-color="{t['accent']}" stop-opacity="0"/>
      <stop offset=".5" stop-color="{t['accent']}" stop-opacity=".18"/>
      <stop offset="1" stop-color="{t['accent']}" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="fade" cx=".3" cy=".5" r=".8">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="m"><rect width="{w}" height="{h}" fill="url(#fade)"/></mask>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="url(#bg)"/>
  <rect width="{w}" height="{h}" rx="18" fill="url(#g)" mask="url(#m)" opacity=".7"/>
  <rect class="scan" x="0" y="0" width="260" height="{h}" fill="url(#beam)"/>

  <text x="96" y="92" class="tag">DEVELOPER · AI INTEGRATION · AUTOMATION</text>
  <text x="92" y="166" class="name">Hồ Hiệp</text>
  <text x="70" y="224" class="prompt">›</text>
  {''.join(typed)}
  {caret}

  <g>
    <circle cx="1000" cy="160" r="104" class="orbit spin"/>
    <circle cx="1000" cy="160" r="72" class="orbit spin2"/>
    <g class="spin"><circle cx="1104" cy="160" r="5" class="dot"/></g>
    <g class="spin2"><circle cx="1000" cy="88" r="4" class="dot" opacity=".7"/></g>
    <g class="pulse">
      <rect x="966" y="126" width="68" height="68" rx="16" fill="{t['accent']}"/>
      <path d="M986 172 L1000 140 L1014 172 M991 162 h18" fill="none" stroke="{t['bg1']}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    </g>
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
