"""The Minecraft diamond axe, traced cell for cell from the game's 16 x 16
item texture (assets/minecraft/textures/item/diamond_axe.png, Java
Edition 1.20.4, read from the InventivetalentDev/minecraft-assets mirror
and thresholded on alpha): a handle rising on the main diagonal into a
head whose bit faces up and left, with the handle's end showing at the
head's lower right. No cell is changed for print: the one standing cell
inside the head opens downward to the face."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import union
from ..motif import Motif

CELL = 1.6  # mm per pixel; 16 cells is 25.6 mm across
ROUND = 0.3  # mm; light open and close so every pixel step shows
ROWS = [  # top row first; # is a cell with alpha above 127 in the game texture, cut
    "................",
    ".........##.....",
    "........####....",
    ".......#####....",
    "......#######...",
    "......#######...",
    ".......#######..",
    "........######..",
    ".......###.##...",
    "......###.......",
    ".....###........",
    "....###.........",
    "...###..........",
    "..###...........",
    "..##............",
    "................",
]


def draw():
    # Cells are unioned on an integer grid so shared edges coincide exactly, then scaled.
    n_rows, n_cols = len(ROWS), len(ROWS[0])
    cells = [box(c, n_rows - r - 1, c + 1, n_rows - r) for r, row in enumerate(ROWS) for c, ch in enumerate(row) if ch == "#"]
    sprite = affinity.translate(union(*cells), -n_cols / 2, -n_rows / 2)
    sprite = affinity.scale(sprite, CELL, CELL, origin=(0, 0))
    return sprite.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(ROUND, 16).buffer(-ROUND, 16)


motif = Motif(name="minecraft_axe", issue=151, draw=draw)
