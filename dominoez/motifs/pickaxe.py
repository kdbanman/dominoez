"""A Minecraft-style pickaxe: the classic 13 x 13 pixel sprite. A two-cell
handle runs from the bottom left up to the top right, into the inside corner
of a Gamma-shaped head whose two arms end in a one-cell tip curl. One-cell
standing gaps separate the handle from both arms near the junction. The
sprite is symmetric under (r, c) -> (12 - c, 12 - r)."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 1.7  # mm per pixel; 13 cells is 22.1 mm across
ROUND = 0.4  # mm; light open and close so the pixels stay crisp
ROWS = [  # top row first; # is cut
    "...##########",
    "...##########",
    "...#.....####",
    "........##.##",
    ".......##..##",
    "......##...##",
    ".....##....##",
    "....##.....##",
    "...##......##",
    "..##......###",
    ".##..........",
    "##...........",
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
