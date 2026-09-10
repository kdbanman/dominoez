import hashlib
import io

import pytest
import trimesh

from dominoez.build import build_motif
from dominoez.body import engrave
from dominoez.motifs import MOTIFS


def test_blank_build_is_deterministic(tmp_path):
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    build_motif(MOTIFS["blank"], a)
    build_motif(MOTIFS["blank"], b)
    for kind, ext in (("stl", "stl"), ("svg", "svg"), ("png", "png")):
        ha = hashlib.sha256((a / kind / f"blank.{ext}").read_bytes()).hexdigest()
        hb = hashlib.sha256((b / kind / f"blank.{ext}").read_bytes()).hexdigest()
        assert ha == hb, kind


@pytest.mark.parametrize("name", list(MOTIFS))
def test_every_motif_stl_is_watertight_after_the_round_trip(name):
    # STL is float32; vertices a hair apart can merge on reload and open the mesh.
    mesh = engrave(MOTIFS[name].geometry())
    data = trimesh.exchange.stl.export_stl(mesh)
    back = trimesh.load(io.BytesIO(data), file_type="stl")
    assert back.is_watertight
    assert back.is_winding_consistent
