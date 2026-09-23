"""A wedge of watermelon, point up: a plump sector with a fat rind band
along the curved bottom edge, parted from the flesh by a thin standing
line, and four big standing seeds in the flesh."""

import math

from shapely.geometry import Point, Polygon

from ..geometry import dot, union
from ..motif import Motif

APEX = (0.0, 10.0)  # the point of the wedge
RADIUS = 22.0  # from the apex to the rind's outer edge
HALF_ANGLE = 34.0  # degrees either side of straight down
RIND = 3.4  # depth of the rind band along the arc
GAP = 1.2  # standing line between rind and flesh
SEEDS = [(0.0, 3.0, 2.6), (-4.5, -2.0, 2.6), (4.5, -2.0, 2.6), (0.0, -5.0, 2.6)]  # standing (u, v, diameter)
ROUND = 0.9  # blunts the point and the rind's corners
STEPS = 32


def _sector(radius):
    au, av = APEX
    a0, a1 = math.radians(-90 - HALF_ANGLE), math.radians(-90 + HALF_ANGLE)
    arc = [(au + radius * math.cos(a0 + (a1 - a0) * i / STEPS), av + radius * math.sin(a0 + (a1 - a0) * i / STEPS)) for i in range(STEPS + 1)]
    return Polygon([APEX, *arc])


def draw():
    whole = _sector(RADIUS).buffer(-ROUND, 16).buffer(ROUND, 16)
    flesh = _sector(RADIUS - RIND - GAP).buffer(-ROUND, 16).buffer(ROUND, 16)
    rind = whole.difference(Point(*APEX).buffer(RADIUS - RIND, 64))
    return union(flesh.difference(union(*(dot(*s) for s in SEEDS))), rind)


motif = Motif(name="watermelon_slice", issue=117, draw=draw)
