"""A tornado funnel: a stack of swirl strokes, each shorter than the one
above, leaning as they narrow to the ground, with debris flung about its foot."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import dot, stroke, union
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
# Debris around the foot, each a wall's width or more clear of the funnel:
# dots as (u, v, diameter) and one tumbling plank as (u, v, length, thickness, degrees).
DEBRIS_DOTS = [(-7.0, -10.5, 2.0), (6.0, -8.5, 1.8), (2.5, -14.5, 2.0), (7.5, -12.5, 1.6)]
PLANK = (-3.5, -15.2, 3.4, 1.6, 25.0)
SAG = 1.0  # how far the middle of the widest swirl dips below its ends, scaled by length


def _swirl(u, v, length, width):
    half = length / 2
    sag = SAG * length / SWIRLS[0][2]
    n = 24
    pts = [(u - half + length * i / n, v - sag * (1 - (2 * i / n - 1) ** 2)) for i in range(n + 1)]
    return stroke(pts, width)


def _plank(u, v, length, thickness, degrees):
    plank = box(-length / 2, -thickness / 2, length / 2, thickness / 2).buffer(-0.5, 8).buffer(0.5, 8)
    return affinity.translate(affinity.rotate(plank, degrees), u, v)


def draw():
    return union(*(_swirl(*s) for s in SWIRLS), *(dot(*d) for d in DEBRIS_DOTS), _plank(*PLANK))


motif = Motif(name="tornado", issue=14, draw=draw)
