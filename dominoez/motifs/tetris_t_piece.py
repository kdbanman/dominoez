"""The Tetris T tetromino pointing up: four fat rounded squares, three in a
row with the fourth centred on top, each cut separately with a wall left
standing between neighbours."""

from shapely import affinity

from ..geometry import rounded_rect, union
from ..motif import Motif

PITCH = 8.6  # mm from one square's centre to the next; three across is 25.8 mm
SQUARE = 7.4  # mm side of each square, leaving a 1.2 mm wall between neighbours
CORNER = 1.2  # mm corner radius on each square
CELLS = [(-1, 0), (0, 0), (1, 0), (0, 1)]  # (column, row) of each square; the top one is the stem


def draw():
    parts = [affinity.translate(rounded_rect(SQUARE, SQUARE, CORNER), c * PITCH, r * PITCH) for c, r in CELLS]
    return union(*parts)


motif = Motif(name="tetris_t_piece", issue=156, draw=draw)
