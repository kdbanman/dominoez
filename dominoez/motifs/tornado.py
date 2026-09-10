"""A tornado funnel: a stack of swirl strokes, each shorter than the one
above, leaning as they narrow to the ground."""

from ..geometry import stroke, union
from ..motif import Motif

# One row per swirl, top first: (centre u, centre v, length, width).
# Rows are far enough apart that a wall above the minimum stands between them.
SWIRLS = [
    (0.0, 12.5, 21.0, 3.2),
    (1.3, 7.7, 16.5, 3.0),
    (2.3, 2.9, 12.5, 2.8),
    (1.8, -1.9, 8.5, 2.6),
    (0.0, -6.7, 5.5, 2.4),
    (-2.2, -11.5, 3.2, 2.2),
]
SAG = 1.0  # how far the middle of the widest swirl dips below its ends, scaled by length


def _swirl(u, v, length, width):
    half = length / 2
    sag = SAG * length / SWIRLS[0][2]
    n = 24
    pts = [(u - half + length * i / n, v - sag * (1 - (2 * i / n - 1) ** 2)) for i in range(n + 1)]
    return stroke(pts, width)


def draw():
    return union(*(_swirl(*s) for s in SWIRLS))


motif = Motif(name="tornado", issue=14, draw=draw)
