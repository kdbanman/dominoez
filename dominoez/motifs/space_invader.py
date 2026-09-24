"""The Space Invaders crab, traced cell for cell from the arcade's 11 x 8
sprite in its arms-down frame: two antennae rising from a wide head, the
eyes standing as single cells, arms out to either side and two legs
below. It faces down the screen, as in the game."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 2.4  # mm per pixel; 11 cells is 26.4 mm across
ROUND = 0.4  # mm; light open and close so the pixels stay crisp
ROWS = [  # top row first; # is cut
    "..#.....#..",
    "...#...#...",
    "..#######..",
    ".##.###.##.",
    "###########",
    "#.#######.#",
    "#.#.....#.#",
    "...##.##...",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "#"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    sprite = affinity.scale(sprite, CELL, CELL, origin=(0, 0))
    return sprite.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(ROUND, 16).buffer(-ROUND, 16)


motif = Motif(name="space_invader", issue=154, draw=draw)
