"""The domino body and the engraving of motifs into it.

Solid coordinates: x across the width, y through the thickness, z up. The foot
sits on z = 0, the body is centred on x = 0 and y = 0. Face A is at y < 0 and
face B at y > 0.
"""

import manifold3d
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.geometry.base import BaseGeometry

from .geometry import rounded_rect
from .spec import BODY, ENGRAVING

_CUT_OVERSHOOT = 0.5  # how far a pocket prism pokes out past the face, so the boolean is clean
_CLEAN = 0.005  # mm; vertices closer than this are merged before extrusion


def _profile() -> list[tuple[float, float]]:
    """(z, inset) pairs describing how far each horizontal slice is shrunk inward."""
    r = BODY.crown_radius
    top = BODY.height
    slices = [(0.0, BODY.foot_chamfer), (BODY.foot_chamfer, 0.0)]
    for theta in np.linspace(0.0, np.pi / 2, 13):
        slices.append((top - r + r * np.sin(theta), r - r * np.cos(theta)))
    return slices


def body() -> trimesh.Trimesh:
    """The blank domino as a watertight convex mesh."""
    base = rounded_rect(BODY.width, BODY.thickness, BODY.edge_radius)
    points = []
    for z, inset in _profile():
        ring = base.buffer(-inset) if inset > 0 else base
        for x, y in ring.exterior.coords:
            points.append((x, y, z))
    hull = manifold3d.Manifold.hull_points(np.asarray(points, dtype=np.float64)).to_mesh()
    return trimesh.Trimesh(hull.vert_properties[:, :3], hull.tri_verts, process=True)


def _face_transform(face: str) -> np.ndarray:
    """Map an extrusion (u, -v, depth) into position on the given face.

    The polygon is drawn with v negated, then rotated -90 degrees about x, which
    sends (u, -v, d) to (u, d, v). Face B also negates u so a viewer standing in
    front of that face reads the motif the right way round.
    """
    rot = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])
    if face == "A":
        shift = trimesh.transformations.translation_matrix(
            [0, -BODY.thickness / 2 - _CUT_OVERSHOOT, BODY.height / 2]
        )
    elif face == "B":
        shift = trimesh.transformations.translation_matrix(
            [0, BODY.thickness / 2 - ENGRAVING.depth, BODY.height / 2]
        )
    else:
        raise ValueError(face)
    return shift @ rot


def _polygons(geom: BaseGeometry) -> list[Polygon]:
    if geom.is_empty:
        return []
    if isinstance(geom, Polygon):
        return [geom]
    return [g for g in geom.geoms if isinstance(g, Polygon) and not g.is_empty]


def pockets(engraved: BaseGeometry) -> list[trimesh.Trimesh]:
    """One prism per polygon per face, positioned to be subtracted from the body."""
    out = []
    for face in ("A", "B"):
        flip_u = -1.0 if face == "B" else 1.0
        transform = _face_transform(face)
        for poly in _polygons(engraved):
            flipped = Polygon(
                [(flip_u * u, -v) for u, v in poly.exterior.coords],
                [[(flip_u * u, -v) for u, v in ring.coords] for ring in poly.interiors],
            )
            # Unions leave near-coincident vertices that break triangulation.
            cleaned = flipped.simplify(_CLEAN, preserve_topology=True)
            prism = trimesh.creation.extrude_polygon(cleaned, ENGRAVING.depth + _CUT_OVERSHOOT)
            if not prism.is_volume:
                raise RuntimeError("pocket prism is not a closed volume; the motif polygon is degenerate")
            prism.apply_transform(transform)
            out.append(prism)
    return out


def engrave(engraved: BaseGeometry) -> trimesh.Trimesh:
    """The body with the motif cut into both faces."""
    solid = body()
    cutters = pockets(engraved)
    if not cutters:
        return solid
    result = trimesh.boolean.difference([solid, *cutters], engine="manifold")
    if not result.is_watertight:
        raise RuntimeError("engraved mesh is not watertight")
    return result
