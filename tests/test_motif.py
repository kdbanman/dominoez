import pytest
from shapely.geometry import Polygon, box

from dominoez.motif import Motif
from dominoez.spec import BODY, ENGRAVING, motif_box_size


def test_motif_centre_of_mass_sits_in_the_middle_of_the_top_half():
    m = Motif(name="t", issue=0, draw=lambda: box(-3, -20, 7, 5))
    placed = m.geometry()
    cx, cy = placed.centroid.coords[0]
    assert cx == pytest.approx(0)
    assert cy == pytest.approx(ENGRAVING.centre_of_mass)
    assert cy == pytest.approx(BODY.height / 4)
    minx, miny, maxx, maxy = placed.bounds
    assert maxy - miny == pytest.approx(25)


def test_lopsided_motif_is_balanced_not_boxed():
    # A shape with all its area on one side: the centroid lands on the centreline, the box does not.
    m = Motif(name="t", issue=0, draw=lambda: box(-3, -2, 3, 2).union(box(3, -2, 12, 0)))
    placed = m.geometry()
    assert placed.centroid.coords[0][0] == pytest.approx(0)
    minx, miny, maxx, maxy = placed.bounds
    assert minx != pytest.approx(-maxx)
    assert (miny + maxy) / 2 != pytest.approx(ENGRAVING.centre_of_mass)


def test_placed_motif_sits_inside_the_box():
    _, bh = motif_box_size()
    assert ENGRAVING.centre_of_mass < bh / 2


def test_blank_stays_empty():
    assert Motif(name="b", issue=0, draw=Polygon).geometry().is_empty
