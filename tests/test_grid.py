import pytest

from dominoez.check import check
from dominoez.geometry import grid
from dominoez.spec import LIMITS, motif_box_size


def test_cut_cells_are_one_wall_apart():
    g = grid(["XX"], "cut")
    pitch = motif_box_size()[0] / 2
    left, right = sorted(g.geoms, key=lambda p: p.centroid.x)
    assert right.bounds[0] - left.bounds[2] == pytest.approx(LIMITS.wall)
    assert left.bounds[2] - left.bounds[0] == pytest.approx(pitch - LIMITS.wall)


def test_cut_grid_is_centred():
    g = grid([".X.", "...", ".X."], "cut")
    minx, miny, maxx, maxy = g.bounds
    assert minx == pytest.approx(-maxx)
    assert miny == pytest.approx(-maxy)


def test_field_grid_leaves_live_cells_standing():
    g = grid(["X.", ".."], "field")
    pitch = motif_box_size()[0] / 2
    assert g.area == pytest.approx(3 * pitch * pitch)
    assert len(g.interiors) == 0  # the standing cell touches the corner, not an island


def test_field_live_cells_merge_into_one_island():
    g = grid(["....", ".XX.", ".XX.", "...."], "field")
    assert len(g.interiors) == 1


def test_ragged_rows_rejected():
    with pytest.raises(ValueError):
        grid(["X", "XX"], "cut")


def test_unknown_style_rejected():
    with pytest.raises(ValueError):
        grid(["X"], "engraved")


@pytest.mark.parametrize("rows, style", [(["X"], "cut"), (["X"], "field"), ([".X.", "..X", "XXX"], "cut")])
def test_grids_are_printable(rows, style):
    assert check(grid(rows, style)) == []
