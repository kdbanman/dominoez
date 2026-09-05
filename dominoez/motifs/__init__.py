"""Registry of every motif. Add a module and list it here."""

from ..motif import Motif
from . import blank, heart

_ALL: list[Motif] = [
    blank.motif,
    heart.motif,
]

MOTIFS: dict[str, Motif] = {m.name: m for m in _ALL}
assert len(MOTIFS) == len(_ALL), "duplicate motif name"
