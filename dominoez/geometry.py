"""2D helpers for drawing motifs.

Motif coordinates: u runs horizontally (positive to the viewer's right), v runs
vertically (positive up), origin at the centre of the face. Units are mm.
"""

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon, box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .spec import BODY, ENGRAVING, LIMITS, motif_box_size


def motif_box() -> Polygon:
    w, h = motif_box_size()
    return box(-w / 2, -h / 2, w / 2, h / 2)


def place(drawn: BaseGeometry) -> BaseGeometry:
    """Put a drawn motif where it goes on the face: centred across, hung from the top.

    Motifs are drawn centred on the origin. On the face they sit high, with the
    top of the motif ENGRAVING.crown_gap below the crown. A blank stays empty.
    """
    if drawn.is_empty:
        return drawn
    assert ENGRAVING.crown_gap >= ENGRAVING.margin, "the motif would cross the motif box"
    minx, miny, maxx, maxy = drawn.bounds
    top = BODY.height / 2 - ENGRAVING.crown_gap
    return affinity.translate(drawn, xoff=-(minx + maxx) / 2, yoff=top - maxy)


def stroke(points: list[tuple[float, float]], width: float, cap: str = "round") -> Polygon:
    """A centreline buffered to a solid stroke. Width is the whole width, not half."""
    cap_style = {"round": 1, "flat": 2, "square": 3}[cap]
    return LineString(points).buffer(width / 2, cap_style=cap_style)


def dot(u: float, v: float, diameter: float) -> Polygon:
    return Point(u, v).buffer(diameter / 2)


def union(*parts: BaseGeometry) -> BaseGeometry:
    return unary_union(list(parts))


def rounded_rect(width: float, height: float, radius: float) -> Polygon:
    """Axis-aligned rectangle centred on the origin with rounded corners."""
    if radius <= 0:
        return box(-width / 2, -height / 2, width / 2, height / 2)
    inner = box(-width / 2 + radius, -height / 2 + radius, width / 2 - radius, height / 2 - radius)
    return inner.buffer(radius)


def grid(rows: list[str], style: str, live: str = "X") -> BaseGeometry:
    """A grid motif. See GUIDELINES.md, "Grid motifs".

    `rows` are strings of equal length, top row first; a `live` character is a
    live cell, anything else is dead. Cell pitch is the motif box width divided
    by the grid width, and the grid is centred on the face.

    style "cut": each live cell is an engraved square, one wall width smaller
    than its pitch, so adjacent live cells are separated by a minimum wall.

    style "field": the whole bounding grid is engraved and live cells stand at
    face level. Adjacent live cells merge into one island.
    """
    if style not in ("cut", "field"):
        raise ValueError(f"unknown grid style {style!r}")
    n_rows = len(rows)
    n_cols = len(rows[0])
    if n_rows == 0 or any(len(r) != n_cols for r in rows):
        raise ValueError("grid rows must be non-empty and all the same length")
    pitch = motif_box_size()[0] / n_cols
    width, height = pitch * n_cols, pitch * n_rows

    def cell(r: int, c: int, inset: float) -> Polygon:
        u0 = -width / 2 + c * pitch
        v1 = height / 2 - r * pitch
        return box(u0 + inset, v1 - pitch + inset, u0 + pitch - inset, v1 - inset)

    if style == "cut":
        return union(*(cell(r, c, LIMITS.wall / 2) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == live))
    field = box(-width / 2, -height / 2, width / 2, height / 2)
    standing = union(*(cell(r, c, 0) for r, row in enumerate(rows) for c, ch in enumerate(row) if ch == live))
    return field.difference(standing)
