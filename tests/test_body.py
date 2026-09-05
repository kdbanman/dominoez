import numpy as np
from shapely.geometry import box

from dominoez.body import body, engrave
from dominoez.spec import BODY, ENGRAVING


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
    assert abs(removed - 2 * 100 * ENGRAVING.depth) < 1.0
