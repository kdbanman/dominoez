"""A Pac-Man ghost, traced cell for cell from the arcade's 14 x 14 sprite:
a domed head, straight sides, and a wavy hem of four feet. It faces left,
so each eye is a standing white with its pupil cut into the lower left
corner, leaving the white as an L."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 1.7  # mm per pixel; 14 cells is 23.8 mm across, as tall as the box allows once the ghost is placed by its centre of mass
ROUND = 0.4  # mm; light open and close so the pixels stay crisp
ROWS = [  # top row first; # is cut, . inside the body is a standing eye white
    ".....####.....",
    "...########...",
    "..##########..",
    ".#...###...##.",
    ".#...###...##.",
    "##.#####.#####",
    "##.#####.#####",
    "##############",
    "##############",
    "##############",
    "##############",
    "##############",
    "##############",
    "##.###..###.##",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "#"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    sprite = affinity.scale(sprite, CELL, CELL, origin=(0, 0))
    return sprite.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(ROUND, 16).buffer(-ROUND, 16)


motif = Motif(name="pac_man_ghost", issue=155, draw=draw)
