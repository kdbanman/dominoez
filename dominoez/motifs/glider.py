"""Conway's Game of Life glider: five live cells in a 3x3 box, cut into an
empty field. This is the phase that points down and to the right."""

from ..geometry import grid
from ..motif import Motif

ROWS = [
    ".X.",
    "..X",
    "XXX",
]

motif = Motif(name="glider", issue=20, draw=lambda: grid(ROWS, "cut"))
