import io
import shutil

import pytest
import trimesh

from dominoez.build import build_motif
from dominoez.cli import main
from dominoez.motifs import MOTIFS
from dominoez.plate import GAP, MARGIN, PLATES, bed, capacity, layout, plate, read, saved, select
from dominoez.spec import BODY


def test_bed_comes_from_the_profile():
    assert bed() == (5.0, 5.0, 295.0, 295.0)


def test_capacity_is_a_full_grid_of_standing_dominoes():
    cols, rows = capacity()
    assert (cols, rows) == (6, 12)
    xmin, ymin, xmax, ymax = bed()
    assert cols * BODY.width + (cols - 1) * GAP <= xmax - xmin - 2 * MARGIN
    assert rows * BODY.thickness + (rows - 1) * GAP <= ymax - ymin - 2 * MARGIN


def test_layout_keeps_every_domino_inside_the_margin_and_apart():
    cols, rows = capacity()
    xmin, ymin, xmax, ymax = bed()
    for count in (1, cols, cols + 1, cols * rows):
        spots = layout(count)
        assert len(spots) == count
        for x, y in spots:
            assert xmin + MARGIN <= x - BODY.width / 2
            assert x + BODY.width / 2 <= xmax - MARGIN
            assert ymin + MARGIN <= y - BODY.thickness / 2
            assert y + BODY.thickness / 2 <= ymax - MARGIN
        for i, (x1, y1) in enumerate(spots):
            for x2, y2 in spots[i + 1 :]:
                assert abs(x1 - x2) >= BODY.width + GAP or abs(y1 - y2) >= BODY.thickness + GAP


def test_layout_is_centred_on_the_bed():
    xmin, ymin, xmax, ymax = bed()
    spots = layout(3)
    assert sum(x for x, _ in spots) / 3 == pytest.approx((xmin + xmax) / 2)
    assert spots[0][1] == pytest.approx((ymin + ymax) / 2)


def test_layout_refuses_more_than_the_bed_holds():
    cols, rows = capacity()
    with pytest.raises(ValueError):
        layout(cols * rows + 1)


def test_plate_needs_built_stls(tmp_path):
    with pytest.raises(FileNotFoundError):
        plate([MOTIFS["blank"]], "p", tmp_path)


def test_plate_stacks_the_built_dominoes_where_layout_puts_them(tmp_path):
    build_motif(MOTIFS["blank"], tmp_path)
    path = plate([MOTIFS["blank"]] * 3, "three", tmp_path)
    assert path == tmp_path / "plate" / "three.stl"
    mesh = trimesh.load(io.BytesIO(path.read_bytes()), file_type="stl")
    single = trimesh.load(tmp_path / "stl" / "blank.stl", file_type="stl")
    assert mesh.volume == pytest.approx(3 * single.volume, rel=1e-6)
    spots = layout(3)
    (xlo, ylo, zlo), (xhi, yhi, zhi) = mesh.bounds
    assert xlo == pytest.approx(min(x for x, _ in spots) - BODY.width / 2, abs=1e-3)
    assert xhi == pytest.approx(max(x for x, _ in spots) + BODY.width / 2, abs=1e-3)
    assert ylo == pytest.approx(spots[0][1] - BODY.thickness / 2, abs=1e-3)
    assert yhi == pytest.approx(spots[0][1] + BODY.thickness / 2, abs=1e-3)
    assert zlo == pytest.approx(0.0, abs=1e-6)
    assert zhi == pytest.approx(BODY.height, abs=1e-3)


def test_counts_follow_names_and_star_is_everything():
    names = [m.name for m in select(["blank", "x3", "heart", "2x", "heart"])]
    assert names == ["blank", "blank", "blank", "heart", "heart", "heart"]
    assert [m.name for m in select(["*"])] == list(MOTIFS)
    assert [m.name for m in select(["*", "x2"])] == list(MOTIFS) + [list(MOTIFS)[-1]]


def test_bad_tokens_are_errors():
    with pytest.raises(ValueError):
        select(["x3"])
    with pytest.raises(ValueError):
        select(["no_such_motif"])


def test_plate_files_are_tokens_with_comments(tmp_path):
    f = tmp_path / "party.txt"
    f.write_text("# a party\nheart x2  # two hearts\nblank\n\n")
    assert [m.name for m in read(f)] == ["heart", "heart", "blank"]


def test_every_saved_plate_reads_and_fits():
    files = saved()
    assert "all" in files
    cols, rows = capacity()
    for name, path in files.items():
        motifs = read(path)
        assert 0 < len(motifs) <= cols * rows, name
    assert [m.name for m in read(files["all"])] == list(MOTIFS)


@pytest.mark.skipif(shutil.which("prusa-slicer") is not None, reason="slicer present, plate would slice")
def test_plate_command_without_a_slicer_writes_the_stl(tmp_path, capsys):
    build_motif(MOTIFS["blank"], tmp_path)
    main(["plate", "blank", "x2", "--name", "pair", "--out", str(tmp_path)])
    out = capsys.readouterr().out
    assert "pair: 2 dominoes on a bed of 6 x 12" in out
    assert "STL only" in out
    assert (tmp_path / "plate" / "pair.stl").exists()


def test_plate_command_with_no_names_needs_every_stl(tmp_path):
    with pytest.raises(SystemExit, match="is missing"):
        main(["plate", "--out", str(tmp_path)])
