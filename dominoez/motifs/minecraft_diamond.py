"""The Minecraft diamond, traced cell for cell from the game's 16 x 16 item
sprite: a gem with a wide flat table, a sharp girdle at its widest two
rows, and a pavilion tapering straight down to a two-cell point. The sprite's white
glint near the top left is left standing as a two by two square. Empty
rows and columns of the sprite are dropped so the cells can be drawn large."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 2.1  # mm per pixel; 12 cells is 25.2 mm across
ROUND = 0.4  # mm; light open and close so the pixels stay crisp
ROWS = [  # top row first; # is cut, o is a standing glint inside the cut
    "..########..",
    ".##########.",
    "##oo########",
    "##oo########",
    ".##########.",
    "..########..",
    "...######...",
    "....####....",
    ".....##.....",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "#"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    sprite = affinity.scale(sprite, CELL, CELL, origin=(0, 0))
    return sprite.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(ROUND, 16).buffer(-ROUND, 16)


motif = Motif(name="minecraft_diamond", issue=153, draw=draw)
