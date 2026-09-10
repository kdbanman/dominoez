import pytest
from shapely.geometry import Polygon, box

from dominoez.motif import Motif
from dominoez.spec import BODY, ENGRAVING, motif_box_size


def test_motif_is_centred_across_and_hung_from_the_top():
    m = Motif(name="t", issue=0, draw=lambda: box(-3, -20, 7, 5))
    minx, miny, maxx, maxy = m.geometry().bounds
    assert minx == pytest.approx(-maxx)
    assert maxy == pytest.approx(BODY.height / 2 - ENGRAVING.crown_gap)
    assert maxy - miny == pytest.approx(25)


def test_placed_motif_sits_inside_the_box():
    _, bh = motif_box_size()
    assert BODY.height / 2 - ENGRAVING.crown_gap <= bh / 2


def test_blank_stays_empty():
    assert Motif(name="b", issue=0, draw=Polygon).geometry().is_empty
