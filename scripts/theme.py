"""Shared look for every generated SVG: palette, fonts, paper grain, tag shape."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

INK = "#14284B"
RED = "#C8102E"
MANILA = "#E6C884"
EDGE = "#C39A52"
KRAFT = "#9C7236"
PAPER = "#F8F0DA"
FAINT = "#14284B33"


def _b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode()


def style(extra=""):
    fonts = ROOT / "scripts" / "fonts"
    return f"""<style>
@font-face{{font-family:Elite;src:url(data:font/woff2;base64,{_b64(fonts / 'elite.woff2')}) format('woff2')}}
@font-face{{font-family:Stencil;src:url(data:font/woff2;base64,{_b64(fonts / 'stencil.woff2')}) format('woff2')}}
text{{font-family:Elite,'Courier New',monospace;fill:{INK}}}
.st{{font-family:Stencil,Impact,sans-serif}}
{extra}
</style>"""


GRAIN = """<filter id="grain" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="8"/>
<feColorMatrix values="0 0 0 0 .3  0 0 0 0 .2  0 0 0 0 .05  0 0 0 .32 -.08"/>
<feComposite in2="SourceGraphic" operator="in"/>
<feBlend in2="SourceGraphic" mode="multiply"/>
</filter>"""


def tag_path(x, y, w, h, c=26):
    """Luggage-style evidence tag: chamfered left corners, punched string hole."""
    hx, hy = x + 27, y + h / 2
    return (f"M{x+c} {y}H{x+w-6}q6 0 6 6V{y+h-6}q0 6-6 6H{x+c}L{x} {y+h-c}V{y+c}Z"
            f"M{hx-8} {hy}a8 8 0 1 0 16 0a8 8 0 1 0-16 0Z")


def tag(x, y, w, h, fill=MANILA):
    hx, hy = x + 27, y + h / 2
    return (f'<path d="{tag_path(x, y, w, h)}" fill="{fill}" fill-rule="evenodd" stroke="{EDGE}" filter="url(#grain)"/>'
            f'<circle cx="{hx}" cy="{hy}" r="13" fill="none" stroke="{EDGE}" stroke-width="5"/>')


def svg(w, h, body, label, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">{style(extra)}<defs>{GRAIN}</defs>{body}</svg>')
