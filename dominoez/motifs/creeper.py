"""The Minecraft creeper face, 8x8. The eyes and mouth are the picture, so
the field is cut and they stand at face level."""

from ..geometry import grid
from ..motif import Motif

ROWS = [
    "........",
    "........",
    ".XX..XX.",
    ".XX..XX.",
    "...XX...",
    "..XXXX..",
    "..XXXX..",
    "..X..X..",
]

motif = Motif(name="creeper", issue=15, draw=lambda: grid(ROWS, "field"))
