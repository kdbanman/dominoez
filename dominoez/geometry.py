"""2D helpers for drawing motifs.

Motif coordinates: u runs horizontally (positive to the viewer's right), v runs
vertically (positive up), origin at the centre of the face. Units are mm.
"""

from shapely.geometry import LineString, Point, Polygon, box
from shapely.geometry.base import BaseGeometry
from shapely.ops import unary_union

from .spec import motif_box_size


def motif_box() -> Polygon:
    w, h = motif_box_size()
    return box(-w / 2, -h / 2, w / 2, h / 2)


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
