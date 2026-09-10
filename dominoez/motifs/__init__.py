"""Registry of every motif. Add a module and list it here."""

from ..motif import Motif
from . import banana, bicycle, blank, creeper, duck, glider, heart, letter_g, r_pentomino, rocket, tornado, toucan

_ALL: list[Motif] = [
    blank.motif,
    heart.motif,
    glider.motif,
    r_pentomino.motif,
    creeper.motif,
    duck.motif,
    banana.motif,
    rocket.motif,
    letter_g.motif,
    toucan.motif,
    tornado.motif,
    bicycle.motif,
]

MOTIFS: dict[str, Motif] = {m.name: m for m in _ALL}
assert len(MOTIFS) == len(_ALL), "duplicate motif name"
