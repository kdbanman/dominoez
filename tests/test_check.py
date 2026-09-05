from shapely.geometry import Point, box

from dominoez.check import check
from dominoez.geometry import stroke


def rules(geom):
    return {v.rule.split(" <")[0] for v in check(geom)}


def test_empty_is_fine():
    assert check(box(0, 0, 0, 0).buffer(0)) == []


def test_fat_square_passes():
    assert check(box(-5, -5, 5, 5)) == []


def test_thin_stroke_fails_channel_rule():
    assert "channel" in rules(stroke([(-5, 0), (5, 0)], 0.8))


def test_stroke_at_minimum_passes():
    assert check(stroke([(-5, 0), (5, 0)], 1.0)) == []


def test_thin_wall_between_two_cuts_fails_wall_rule():
    two = box(-6, -3, -0.4, 3).union(box(0.4, -3, 6, 3))
    assert "wall" in rules(two)


def test_wall_at_minimum_passes():
    two = box(-6, -3, -0.5, 3).union(box(0.5, -3, 6, 3))
    assert check(two) == []


def test_small_island_fails_island_rule():
    ring = Point(0, 0).buffer(6).difference(Point(0, 0).buffer(0.6))
    assert "island" in rules(ring)


def test_island_at_minimum_passes():
    ring = Point(0, 0).buffer(6).difference(Point(0, 0).buffer(0.75))
    assert check(ring) == []


def test_outside_motif_box_fails():
    assert "motif box" in rules(box(-20, -5, 20, 5))
