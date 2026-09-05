import numpy as np
from shapely.geometry import box

from dominoez.body import body, engrave
from dominoez.spec import BODY, ENGRAVING, TEXTURE


def test_body_is_a_watertight_convex_slab():
    m = body()
    assert m.is_watertight
    assert m.is_volume
    size = m.bounds[1] - m.bounds[0]
    assert np.allclose(size, [BODY.width, BODY.thickness, BODY.height], atol=1e-6)
    assert m.bounds[0][2] == 0.0
    full = BODY.width * BODY.thickness * BODY.height
    assert 0.95 * full < m.volume < full


def test_engraving_is_mirrored_so_each_face_reads_correctly():
    # A square in the upper-right quadrant as seen by a viewer of either face.
    square = box(6, 8, 10, 12)
    m = engrave(square)
    assert m.is_watertight
    half_depth = ENGRAVING.depth / 2
    y_a = -BODY.thickness / 2 + half_depth
    y_b = BODY.thickness / 2 - half_depth
    z = BODY.height / 2 + 10
    # Face A is viewed from -y, so viewer's right is +x.
    # Face B is viewed from +y, so viewer's right is -x.
    probes = np.array(
        [
            [8, y_a, z],  # face A pocket
            [-8, y_a, z],  # face A solid
            [-8, y_b, z],  # face B pocket
            [8, y_b, z],  # face B solid
        ]
    )
    inside = m.contains(probes)
    assert list(inside) == [False, True, False, True]
    assert m.volume < body().volume


def test_engraving_removes_the_expected_volume():
    square = box(-5, -5, 5, 5)
    removed = body().volume - engrave(square).volume
    shallow = 2 * 100 * (ENGRAVING.depth - TEXTURE.amplitude)
    deep = 2 * 100 * (ENGRAVING.depth + TEXTURE.amplitude)
    assert shallow < removed < deep
    assert abs(removed - 2 * 100 * ENGRAVING.depth) < 2 * 100 * TEXTURE.amplitude / 2


def test_pocket_floor_carries_the_bump_lattice():
    from dominoez.body import floor_depth

    # The origin is a bump top (shallowest). Find the deepest point numerically.
    us = np.linspace(-6, 6, 241)
    gu, gv = np.meshgrid(us, us, indexing="ij")
    d = floor_depth(gu, gv)
    assert abs(d[120, 120] - (ENGRAVING.depth - TEXTURE.amplitude)) < 1e-9
    i, j = np.unravel_index(np.argmax(d), d.shape)
    assert abs(d[i, j] - (ENGRAVING.depth + TEXTURE.amplitude)) < 1e-3

    m = engrave(box(-6, -6, 6, 6))
    y_face = -BODY.thickness / 2
    z0 = BODY.height / 2
    shallow_probe = [0, y_face + ENGRAVING.depth - TEXTURE.amplitude * 0.6, z0]
    deep_probe = [gu[i, j], y_face + ENGRAVING.depth + TEXTURE.amplitude * 0.6, z0 + gv[i, j]]
    inside = m.contains(np.array([shallow_probe, deep_probe]))
    assert list(inside) == [True, False]


def test_lattice_rows_are_offset_by_half_a_bump():
    from dominoez.body import floor_depth

    s = TEXTURE.spacing
    row_height = s * np.sqrt(3) / 2 * TEXTURE.row_squash
    tops = ENGRAVING.depth - TEXTURE.amplitude
    assert abs(floor_depth(np.array(s), np.array(0.0)) - tops) < 1e-9  # neighbour in the same row
    assert abs(floor_depth(np.array(s / 2), np.array(row_height)) - tops) < 1e-9  # next row, offset
    assert floor_depth(np.array(0.0), np.array(row_height)) > tops + TEXTURE.amplitude  # not directly above



def test_engraving_a_union_with_near_duplicate_vertices():
    # Circles unioned with a square leave vertices a hair apart; the pocket must still close.
    from shapely.geometry import Point

    shape = box(-5, -5, 5, 5).union(Point(-5, 5).buffer(5)).union(Point(5, 5).buffer(5))
    m = engrave(shape)
    assert m.is_watertight
    removed = body().volume - m.volume
    assert abs(removed - 2 * ENGRAVING.depth * shape.area) < 2 * shape.area * TEXTURE.amplitude


def test_engraving_a_hole_that_touches_the_exterior_at_a_point():
    # Two standing squares meeting corner to corner, as in a field-cut grid motif.
    shape = box(-8, -8, 8, 8).difference(box(-4, -4, 0, 0)).difference(box(0, 0, 8, 4))
    assert shape.is_valid and len(shape.interiors) == 1
    m = engrave(shape)
    assert m.is_watertight
    removed = body().volume - m.volume
    assert abs(removed - 2 * ENGRAVING.depth * shape.area) < 2 * shape.area * TEXTURE.amplitude
