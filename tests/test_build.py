import hashlib

from dominoez.build import build_motif
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
