"""The domino body and the engraving of motifs into it.

Solid coordinates: x across the width, y through the thickness, z up. The foot
sits on z = 0, the body is centred on x = 0 and y = 0. Face A is at y < 0 and
face B at y > 0.
"""

import manifold3d
import numpy as np
import trimesh
from shapely.geometry import Polygon
from shapely.ops import unary_union
from shapely.geometry.base import BaseGeometry

from .geometry import rounded_rect
from .spec import BODY, ENGRAVING, TEXTURE, motif_box_size

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


def floor_depth(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Engraving depth at each (u, v): shallowest on the bumps, deepest in the gaps.

    The sum of three cosines whose wave vectors are 60 degrees apart peaks on a
    triangular lattice. With wave vectors of length k the lattice spacing is
    (2 / sqrt(3)) * (2 pi / k), so k is chosen from the requested spacing. The
    sum ranges from -1.5 (gaps) to 3 (bump tops); it is rescaled so depth spans
    exactly mean - amplitude (bump top) to mean + amplitude (gap). Rows are
    compressed vertically by TEXTURE.row_squash.
    """
    k = 2 * np.pi / (TEXTURE.spacing * np.sqrt(3) / 2)
    v = v / TEXTURE.row_squash  # squeeze the rows together, stretching bumps sideways
    # Wave vectors at 90, 30 and 150 degrees put the bump rows along u.
    s = (
        np.cos(k * v)
        + np.cos(k * (u * np.sqrt(3) / 2 + v / 2))
        + np.cos(k * (u * np.sqrt(3) / 2 - v / 2))
    )
    relief = (s + 1.5) / 4.5  # 0 in the gaps, 1 on the bump tops
    return ENGRAVING.depth + TEXTURE.amplitude - 2 * TEXTURE.amplitude * relief


def _floor_solid() -> trimesh.Trimesh:
    """A slab, in the extrusion frame, whose top surface is the textured pocket floor.

    Intersecting a pocket prism with this slab gives the prism a wavy floor while
    leaving its walls straight. The lattice is symmetric under u -> -u and
    v -> -v, so the same slab serves both faces despite the u flip.
    """
    w, h = motif_box_size()
    pad = TEXTURE.step * 2
    xs = np.arange(-w / 2 - pad, w / 2 + pad + TEXTURE.step / 2, TEXTURE.step)
    ys = np.arange(-h / 2 - pad, h / 2 + pad + TEXTURE.step / 2, TEXTURE.step)
    gx, gy = np.meshgrid(xs, ys, indexing="ij")
    # The extrusion frame is (u, -v, depth): the slab's y is -v; the lattice is even in v.
    top = _CUT_OVERSHOOT + floor_depth(gx, -gy)
    bottom = np.full_like(top, -1.0)
    nx, ny = gx.shape
    verts = np.concatenate(
        [
            np.column_stack([gx.ravel(), gy.ravel(), top.ravel()]),
            np.column_stack([gx.ravel(), gy.ravel(), bottom.ravel()]),
        ]
    )
    n = nx * ny

    def idx(i, j, layer=0):
        return layer * n + i * ny + j

    i, j = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1), indexing="ij")
    i, j = i.ravel(), j.ravel()
    a, b, c, d = idx(i, j), idx(i + 1, j), idx(i + 1, j + 1), idx(i, j + 1)
    top_faces = np.concatenate([np.column_stack([a, b, c]), np.column_stack([a, c, d])])
    bottom_faces = top_faces[:, ::-1] + n
    sides = []
    for ring in (
        [idx(i, 0) for i in range(nx)],  # y min edge
        [idx(nx - 1, j) for j in range(ny)],  # x max edge
        [idx(i, ny - 1) for i in range(nx - 1, -1, -1)],  # y max edge
        [idx(0, j) for j in range(ny - 1, -1, -1)],  # x min edge
    ):
        for p, q in zip(ring[:-1], ring[1:]):
            sides.append([p, q + n, q])
            sides.append([p, p + n, q + n])
    faces = np.concatenate([top_faces, bottom_faces, np.array(sides)])
    slab = trimesh.Trimesh(verts, faces, process=False)
    if slab.volume < 0:
        slab.invert()
    if not slab.is_volume:
        raise RuntimeError("floor slab is not a closed volume")
    return slab


def _unpinch(poly: Polygon) -> list[Polygon]:
    """Part any rings of `poly` that touch at a point.

    A hole touching the exterior, or another hole, at a single point is valid
    shapely but defeats the triangulation behind the extrusion. Standing cells
    that meet corner to corner (a field-cut grid motif) do exactly this. Filling
    a hair-sized disc of the cut at each such point joins the rings through a
    bridge of standing material far too small for the nozzle to notice.
    """
    rings = [poly.exterior, *poly.interiors]
    touches = [a.intersection(b) for i, a in enumerate(rings) for b in rings[i + 1 :]]
    touches = [t for t in touches if not t.is_empty]
    if not touches:
        return [poly]
    return _polygons(poly.difference(unary_union(touches).buffer(_CLEAN * 2)))


def pockets(engraved: BaseGeometry) -> list[trimesh.Trimesh]:
    """One textured prism per polygon per face, positioned to be subtracted from the body."""
    polys = _polygons(engraved)
    if not polys:
        return []
    floor = _floor_solid()
    out = []
    for face in ("A", "B"):
        flip_u = -1.0 if face == "B" else 1.0
        transform = _face_transform(face)
        for poly in polys:
            flipped = Polygon(
                [(flip_u * u, -v) for u, v in poly.exterior.coords],
                [[(flip_u * u, -v) for u, v in ring.coords] for ring in poly.interiors],
            )
            # Unions leave near-coincident vertices that break triangulation.
            cleaned = flipped.simplify(_CLEAN, preserve_topology=True)
            for piece in _unpinch(cleaned):
                prism = trimesh.creation.extrude_polygon(
                    piece, _CUT_OVERSHOOT + ENGRAVING.depth + TEXTURE.amplitude + 0.1
                )
                if not prism.is_volume:
                    raise RuntimeError("pocket prism is not a closed volume; the motif polygon is degenerate")
                prism = trimesh.boolean.intersection([prism, floor], engine="manifold")
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
