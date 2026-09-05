"""Printability checks. See GUIDELINES.md, "Printability rules"."""

from dataclasses import dataclass

from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from .geometry import motif_box
from .spec import LIMITS


_TOLERANCE = 0.005  # so a feature exactly at the minimum passes


@dataclass(frozen=True)
class Violation:
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def _polygons(geom: BaseGeometry) -> list[Polygon]:
    if geom.is_empty:
        return []
    if isinstance(geom, Polygon):
        return [geom]
    return [g for g in getattr(geom, "geoms", []) if isinstance(g, Polygon) and not g.is_empty]


def _too_thin(region: BaseGeometry, minimum: float) -> list[Polygon]:
    """Pieces of `region` that vanish when it is opened by `minimum`.

    Opening (erode then dilate) removes anything narrower than `minimum`. What
    is left over is material the nozzle cannot make. Tiny corner shavings are
    ignored via LIMITS.residual_area.
    """
    r = minimum / 2 - _TOLERANCE
    opened = region.buffer(-r).buffer(r)
    residual = region.difference(opened)
    return [p for p in _polygons(residual) if p.area > LIMITS.residual_area]


def _describe(pieces: list[Polygon]) -> str:
    worst = max(pieces, key=lambda p: p.area)
    cx, cy = worst.centroid.coords[0]
    return f"{len(pieces)} piece(s), largest {worst.area:.2f} mm^2 near u={cx:.1f}, v={cy:.1f}"


def check(engraved: BaseGeometry) -> list[Violation]:
    """Return every rule the engraved region breaks. Empty list means printable."""
    violations: list[Violation] = []
    if engraved.is_empty:
        return violations

    if not engraved.is_valid:
        violations.append(Violation("valid", "engraved geometry is self-intersecting or malformed"))
        engraved = engraved.buffer(0)

    bx = motif_box()
    outside = engraved.difference(bx.buffer(1e-6))
    if not outside.is_empty and outside.area > 1e-6:
        minx, miny, maxx, maxy = engraved.bounds
        violations.append(
            Violation(
                "motif box",
                f"motif bounds u=[{minx:.1f}, {maxx:.1f}] v=[{miny:.1f}, {maxy:.1f}] "
                f"exceed the box {list(bx.bounds)}",
            )
        )

    thin_cuts = _too_thin(engraved, LIMITS.channel)
    if thin_cuts:
        violations.append(Violation(f"channel < {LIMITS.channel} mm", _describe(thin_cuts)))

    # Standing material: everything in a generous field around the box that is not cut.
    field = bx.buffer(LIMITS.island * 2)
    standing = field.difference(engraved)
    standing_parts = _polygons(standing)
    outer = [p for p in standing_parts if p.intersects(field.exterior)]
    islands = [p for p in standing_parts if not p.intersects(field.exterior)]

    thin_walls = [piece for part in outer for piece in _too_thin(part, LIMITS.wall)]
    if thin_walls:
        violations.append(Violation(f"wall < {LIMITS.wall} mm", _describe(thin_walls)))

    small_islands = [piece for part in islands for piece in _too_thin(part, LIMITS.island)]
    if small_islands:
        violations.append(Violation(f"island < {LIMITS.island} mm", _describe(small_islands)))

    return violations
