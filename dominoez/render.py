"""Review renders: the whole face at true scale, as SVG and PNG."""

from pathlib import Path

import cairosvg
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from .spec import BODY, ENGRAVING, motif_box_size

PAD = 4.0  # mm of canvas around the face
PX_PER_MM = 10


def _fmt(x: float) -> str:
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return "0" if s == "-0" else s


def _to_svg(u: float, v: float) -> tuple[float, float]:
    return PAD + BODY.width / 2 + u, PAD + BODY.height / 2 - v


def _ring(coords) -> str:
    pts = [_to_svg(u, v) for u, v in coords]
    head = f"M{_fmt(pts[0][0])} {_fmt(pts[0][1])}"
    body = "".join(f"L{_fmt(x)} {_fmt(y)}" for x, y in pts[1:-1])
    return head + body + "Z"


def _path(geom: BaseGeometry) -> str:
    polys = [geom] if isinstance(geom, Polygon) else [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon)]
    return "".join(_ring(p.exterior.coords) + "".join(_ring(r.coords) for r in p.interiors) for p in polys)


def svg(engraved: BaseGeometry) -> str:
    w, h = BODY.width, BODY.height
    cw, ch = w + 2 * PAD, h + 2 * PAD
    bw, bh = motif_box_size()
    bx, by = _to_svg(-bw / 2, bh / 2)
    _, chamfer_y = _to_svg(0, -h / 2 + BODY.foot_chamfer)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{_fmt(cw)}" height="{_fmt(ch)}" viewBox="0 0 {_fmt(cw)} {_fmt(ch)}">',
        f'<rect width="{_fmt(cw)}" height="{_fmt(ch)}" fill="#fff"/>',
        f'<rect x="{_fmt(PAD)}" y="{_fmt(PAD)}" width="{_fmt(w)}" height="{_fmt(h)}" rx="{_fmt(BODY.edge_radius)}" fill="#f4f4f4" stroke="#888" stroke-width="0.3"/>',
        f'<line x1="{_fmt(PAD)}" y1="{_fmt(chamfer_y)}" x2="{_fmt(PAD + w)}" y2="{_fmt(chamfer_y)}" stroke="#bbb" stroke-width="0.2"/>',
        f'<rect x="{_fmt(bx)}" y="{_fmt(by)}" width="{_fmt(bw)}" height="{_fmt(bh)}" fill="none" stroke="#c44" stroke-width="0.2" stroke-dasharray="1 1"/>',
    ]
    if not engraved.is_empty:
        parts.append(f'<path d="{_path(engraved)}" fill="#000" fill-rule="evenodd"/>')
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write(engraved: BaseGeometry, svg_path: Path, png_path: Path) -> None:
    text = svg(engraved)
    svg_path.write_text(text)
    cairosvg.svg2png(bytestring=text.encode(), write_to=str(png_path), scale=PX_PER_MM)
