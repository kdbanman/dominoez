"""The tenting cradle: each part prints, the plate fits its pocket, and the cutouts are where they should be."""

import math

import pytest
from manifold3d import CrossSection, JoinType, Manifold

from tenting import parts as P
from tenting import spec as S


@pytest.mark.parametrize("name", list(P.PRINTED))
def test_part_is_a_printable_solid(name):
    m = P.PRINTED[name]()
    assert m.status().name == "NoError"
    assert m.volume() > 0
    x0, y0, z0, x1, y1, _ = m.bounding_box()
    assert z0 == pytest.approx(0, abs=1e-6), "sits on the bed"
    assert max(x1 - x0, y1 - y0) < S.BED


@pytest.mark.parametrize("left, right", [("cradle_left", "cradle_right"), ("test_fit_left", "test_fit_right")])
def test_right_is_the_left_mirrored(left, right):
    assert P.PRINTED[right]().volume() == pytest.approx(P.PRINTED[left]().volume(), rel=1e-6)


def plate_in_cradle(grow=0.0) -> Manifold:
    """The plate's outline, grown by `grow`, as a slab from its feet up past the lip, seated in the cradle."""
    slab = P.outline().offset(grow, JoinType.Round, circular_segments=64).extrude(S.LIP + 5)
    return slab.transform(P.plate_transform()[:3])


def test_plate_drops_in_with_the_slop_all_round():
    cradle = P.cradle_left()
    assert (cradle ^ plate_in_cradle()).volume() < 1e-3
    assert (cradle ^ plate_in_cradle(S.SLOP - 0.05)).volume() < 1e-3
    assert (cradle ^ plate_in_cradle(S.SLOP + 0.1)).volume() > 1.0, "no more than the slop"


def test_plate_is_tented_and_the_pivot_floor_is_thin():
    t = P.plate_transform()
    normal = t[:3, :3] @ [0, 0, 1]
    assert math.degrees(math.acos(normal[2])) == pytest.approx(S.TILT)
    # the pocket's outermost pinky point, on the floor, is FLOOR above the desk
    corner = t[:3, :3] @ [P.pivot_x(), 0, -S.FEET] + t[:3, 3]
    assert corner[2] == pytest.approx(S.FLOOR)


@pytest.mark.parametrize("name", list(S.NOTCHES))
def test_lip_is_cut_to_the_floor_at_each_notch(name):
    x0, y0, x1, y1 = S.NOTCHES[name]
    band = P.rim() - P.pocket()  # where the lip stands
    cut = band ^ CrossSection.square((x1 - x0, y1 - y0)).translate([x0, y0])
    assert cut.area() > 10, "the notch crosses the lip"
    above_floor = cut.extrude(P.TOP).translate([0, 0, 0.01])
    assert (P.tray(S.DECK) ^ above_floor).volume() < 1e-3


def test_desk_foot_pockets_sit_under_solid_wedge():
    """Four distinct pockets, each with at least 1.5 mm of wedge over its ceiling and
    DESK_FOOT_MARGIN of base around it."""
    body = P.desk_cut(P.tilt(P.tray(S.DECK)) + P.wedge())
    feet = P.desk_feet(body)
    assert len({(round(x), round(y)) for x, y in feet}) == 4
    base = body.slice(0.1)
    r = S.DESK_FOOT_D / 2
    for x, y in feet:
        roof = Manifold.cylinder(S.DESK_FOOT_DEPTH + 1.5, r, r, 64).translate([x, y, 0])
        assert (roof - body).volume() < 0.5, f"pocket at ({x:.0f}, {y:.0f}) breaks through the wedge"
        ring = CrossSection.circle(r + S.DESK_FOOT_MARGIN - 0.05, 64).translate([x, y])
        assert (ring - base).area() < 1e-3, f"pocket at ({x:.0f}, {y:.0f}) is too close to the edge"
