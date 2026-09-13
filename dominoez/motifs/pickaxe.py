"""A Minecraft-style pickaxe: a stair-stepped pixel sprite. A two-cell
handle runs from the bottom left up to the top right, where a thicker,
gently bowed head crosses it at right angles, symmetric about the handle,
with both tips curving back toward the handle's foot."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 1.4  # mm per pixel
ROWS = [  # top row first; X is cut
    "......XX.........",
    "......XXXX.......",
    "......XXXXX......",
    "........XXXXX....",
    ".........XXXXX...",
    "..........XXXX...",
    ".........XX.XXX..",
    "........XX..XXXX.",
    ".......XX....XXX.",
    "......XX......XX.",
    ".....XX.......XX.",
    "....XX...........",
    "...XX............",
    "..XX.............",
    ".XX..............",
    "XX...............",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "X"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    return affinity.scale(sprite, CELL, CELL, origin=(0, 0))


motif = Motif(name="pickaxe", issue=36, draw=draw)
