"""Registry of every motif. Add a module and list it here."""

from ..motif import Motif
from . import (
    banana,
    bicycle,
    blank,
    cat_face,
    creeper,
    dog_face,
    duck,
    gamepad,
    glider,
    heart,
    kiwi,
    letter_g,
    letter_i,
    pickaxe,
    r_pentomino,
    rainbow,
    rocket,
    speaker,
    toilet,
    tornado,
    toucan,
    train,
    truck,
    unicorn,
)

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
    toilet.motif,
    cat_face.motif,
    dog_face.motif,
    train.motif,
    truck.motif,
    speaker.motif,
    gamepad.motif,
    kiwi.motif,
    letter_i.motif,
    rainbow.motif,
    unicorn.motif,
    pickaxe.motif,
]

MOTIFS: dict[str, Motif] = {m.name: m for m in _ALL}
assert len(MOTIFS) == len(_ALL), "duplicate motif name"
