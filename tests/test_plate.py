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


def _names(tokens):
    motifs, overrides = select(tokens)
    return [m.name for m in motifs]


def test_counts_follow_names_and_star_is_everything():
    assert _names(["blank", "x3", "heart", "2x", "heart"]) == ["blank", "blank", "blank", "heart", "heart", "heart"]
    assert _names(["*"]) == list(MOTIFS)
    assert _names(["*", "x2"]) == list(MOTIFS) + [list(MOTIFS)[-1]]
    assert select(["blank"])[1] == {}


def test_settings_become_profile_overrides():
    motifs, overrides = select(["brim=4", "blank", "x2"])
    assert [m.name for m in motifs] == ["blank", "blank"]
    assert overrides == {"brim_width": "4"}
    assert select(["blank", "brim=2.5"])[1] == {"brim_width": "2.5"}


def test_bad_tokens_are_errors():
    with pytest.raises(ValueError):
        select(["x3"])
    with pytest.raises(ValueError):
        select(["no_such_motif"])
    with pytest.raises(ValueError, match="unknown setting"):
        select(["blank", "skirt=2"])
    with pytest.raises(ValueError, match="millimetres"):
        select(["blank", "brim=wide"])


def test_plate_files_are_tokens_with_comments(tmp_path):
    f = tmp_path / "party.txt"
    f.write_text("# a party\nheart x2  # two hearts\nblank\nbrim=4  # it keeps lifting\n")
    motifs, overrides = read(f)
    assert [m.name for m in motifs] == ["heart", "heart", "blank"]
    assert overrides == {"brim_width": "4"}


def test_every_saved_plate_reads_and_fits():
    files = saved()
    assert files
    cols, rows = capacity()
    for name, path in files.items():
        motifs, _ = read(path)
        assert 0 < len(motifs) <= cols * rows, name


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
