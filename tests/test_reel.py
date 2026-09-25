"""The reel's parts: each prints, fits the bed, and nothing collides as the reel swings."""

from itertools import combinations

import numpy as np
import pytest

from reel import parts as P
from reel import plates
from reel import spec as S
from reel import views

BED = 290.0


@pytest.mark.parametrize("name", list(P.PRINTED))
def test_part_is_a_printable_solid(name):
    m = P.PRINTED[name]()
    assert m.status().name == "NoError"
    assert m.volume() > 0
    x0, y0, z0, x1, y1, z1 = m.bounding_box()
    assert z0 == pytest.approx(0, abs=1e-6), "sits on the bed"
    assert max(x1 - x0, y1 - y0) < BED


def overhang_area(m, limit_deg=45.0):
    mm = m.to_mesh()
    v = np.asarray(mm.vert_properties)[:, :3]
    t = v[np.asarray(mm.tri_verts)]
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    area = np.linalg.norm(n, axis=1) / 2
    n /= np.maximum(2 * area, 1e-12)[:, None]
    on_bed = np.all(np.abs(t[:, :, 2]) < 1e-6, axis=1)
    steep = (n[:, 2] < -np.cos(np.radians(limit_deg)) - 1e-3) & ~on_bed
    return area[steep].sum()


@pytest.mark.parametrize("name, allowed", [
    ("chassis", 2 * S.XI * 2 * S.BRIDGE_R),   # the bridge's flat underside, bridged between the cheeks
    ("wheel", 15.0),                           # top of the line anchor hole
    ("axle_tube", 60.0),                       # the snap lip's ledge
    ("hanger_shaft", 0.0),
    ("crank", 0.0),
    ("lock_pin", 60.0), ("hinge_pin", 60.0), ("cross_pin", 30.0),  # a lying pin's first millimetre
])
def test_no_overhangs_but_the_known_ones(name, allowed):
    assert overhang_area(P.PRINTED[name]()) <= allowed + 1.0


@pytest.mark.parametrize("tilt", [0.0, S.LOADED_TILT, -S.LOADED_TILT, 60.0, -60.0])
def test_nothing_collides_as_the_reel_swings(tilt):
    parts = views.assembly(tilt=tilt, with_line=False)
    for (a, ma), (b, mb) in combinations(parts, 2):
        assert (ma ^ mb).volume() < 0.01, f"{a} hits {b} at {tilt} degrees"


def test_loaded_line_hangs_under_the_hinge_pin():
    # the tilt puts the axle FLOOR_R to the side of the pin, so the groove's edge is right under it
    assert S.PIVOT_Z * np.sin(np.radians(S.LOADED_TILT)) == pytest.approx(S.FLOOR_R)


def test_crank_clears_the_plywood_when_loaded():
    axle_z = S.PIVOT_Z * (1 - np.cos(np.radians(S.LOADED_TILT)))
    reach = S.CRANK + S.CRANK_HEX_AF  # knob centre plus its corner
    assert S.BOARD_Z - axle_z > reach


def test_the_tube_threads_through():
    # the snap-side bearing passes the wheel's hex bore, the hex passes the head-side cheek's hole
    assert S.BEAR_SNAP < S.WHEEL_HEX_AF
    assert S.TUBE_HEX_AF / np.cos(np.radians(30)) < S.BEAR_HEAD + S.BEAR_CLEAR


def test_shaft_fits_the_shelf_hole():
    corners = S.SHAFT_AF / np.cos(np.radians(22.5))
    assert corners < S.BOARD_HOLE


@pytest.mark.parametrize("name", list(plates.PLATES))
def test_plate_fits_the_bed(name):
    builders, _ = plates.PLATES[name]
    placed = plates.arrange({n: f() for n, f in builders.items()})  # raises if it overflows
    assert set(placed) == set(builders)
