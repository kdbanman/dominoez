from pathlib import Path

from . import render
from .body import engrave
from .check import Violation, check
from .motif import Motif

REPO = Path(__file__).resolve().parents[1]


class Unprintable(Exception):
    def __init__(self, motif: Motif, violations: list[Violation]):
        self.motif = motif
        self.violations = violations
        lines = "\n".join(f"  - {v}" for v in violations)
        super().__init__(f"motif '{motif.name}' breaks printability rules:\n{lines}")


def render_motif(motif: Motif, out: Path = REPO) -> None:
    geom = motif.geometry()
    problems = check(geom)
    if problems:
        raise Unprintable(motif, problems)
    (out / "svg").mkdir(parents=True, exist_ok=True)
    (out / "png").mkdir(parents=True, exist_ok=True)
    render.write(geom, out / "svg" / f"{motif.name}.svg", out / "png" / f"{motif.name}.png")


def build_motif(motif: Motif, out: Path = REPO) -> None:
    render_motif(motif, out)
    geom = motif.geometry()
    (out / "stl").mkdir(parents=True, exist_ok=True)
    mesh = engrave(geom)
    mesh.export(out / "stl" / f"{motif.name}.stl", file_type="stl")
