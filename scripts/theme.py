"""Shared look for every generated SVG: modern dark palette, clean typography, rounded cards."""
import base64
from pathlib import Path
from xml.sax.saxutils import escape as esc

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"

INK = "#f1f5f9"
RED = "#38bdf8"
MANILA = "#161b22"
EDGE = "#30363d"
KRAFT = "#0d1117"
PAPER = "#0d1117"
FAINT = "#30363d88"


def style(extra=""):
    return f"""<style>
text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'JetBrains Mono',monospace;fill:{INK}}}
.st{{font-weight:700;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}}
{extra}
</style>"""


GRAIN = ""


def tag_path(x, y, w, h, r=12):
    return (f"M{x+r} {y}h{w-2*r}a{r} {r} 0 0 1 {r} {r}v{h-2*r}a{r} {r} 0 0 1 -{r} {r}"
            f"h-{w-2*r}a{r} {r} 0 0 1 -{r} -{r}v-{h-2*r}a{r} {r} 0 0 1 {r} -{r}z")


def tag(x, y, w, h, fill=MANILA):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}" stroke="{EDGE}" stroke-width="1.5"/>'


def svg(w, h, body, label, extra=""):
    grain_def = f"<defs>{GRAIN}</defs>" if GRAIN else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{esc(label)}">{style(extra)}{grain_def}{body}</svg>')
