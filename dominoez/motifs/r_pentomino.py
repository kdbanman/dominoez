"""Conway's Game of Life R-pentomino: the five-cell methuselah that runs for
1103 generations. Live cells cut into an empty field."""

from ..geometry import grid
from ..motif import Motif

ROWS = [
    ".XX",
    "XX.",
    ".X.",
]

motif = Motif(name="r_pentomino", issue=21, draw=lambda: grid(ROWS, "cut"))
