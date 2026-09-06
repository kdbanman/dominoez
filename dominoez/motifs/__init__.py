"""Registry of every motif. Add a module and list it here."""

from ..motif import Motif
from . import blank, creeper, glider, heart, r_pentomino

_ALL: list[Motif] = [
    blank.motif,
    heart.motif,
    glider.motif,
    r_pentomino.motif,
    creeper.motif,
]

MOTIFS: dict[str, Motif] = {m.name: m for m in _ALL}
assert len(MOTIFS) == len(_ALL), "duplicate motif name"
