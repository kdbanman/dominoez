"""A Minecraft-style pickaxe, traced cell for cell from the game's 13 x 13
item sprite: a three-cell-wide stair-stepped handle from the bottom left up
to the top right, into a hooked head whose arms sweep left and down, with a
one-cell standing gap between the handle and the lower arm."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 1.7  # mm per pixel; 13 cells is 22.1 mm across
ROUND = 0.4  # mm; light open and close so the pixels stay crisp
ROWS = [  # top row first; # is cut
    "....#####....",
    "...#########.",
    "....########.",
    "........####.",
    ".......######",
    "......###.###",
    ".....###..###",
    "....###...###",
    "...###....###",
    "..###......#.",
    ".###.........",
    "###..........",
    "##...........",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "#"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    sprite = affinity.scale(sprite, CELL, CELL, origin=(0, 0))
    # Open to blunt the outer corners, close to soften the inner ones.
    return sprite.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(ROUND, 16).buffer(-ROUND, 16)


motif = Motif(name="pickaxe", issue=36, draw=draw)
