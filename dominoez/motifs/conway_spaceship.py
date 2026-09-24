"""Conway's Game of Life lightweight spaceship: nine live cells in a 5 x 4
box, cut into an empty field, in the phase that travels left. Drawn like
the glider and R-pentomino, live cells cut with a wall between neighbours."""

from ..geometry import grid
from ..motif import Motif

PITCH = 5.1  # mm per cell; five across is 25.5 mm, the most the box allows since the pattern is lopsided and placed by its centre of mass

ROWS = [
    ".X..X",
    "X....",
    "X...X",
    "XXXX.",
]

motif = Motif(name="conway_spaceship", issue=157, draw=lambda: grid(ROWS, "cut", pitch=PITCH))
