"""A slice of pizza, point down: a plump wedge with a fat crust band along
the curved top, parted from the cheese by a thin standing line, and three
big standing pepperoni on the cheese."""

import math

from shapely.geometry import Polygon, Point

from ..geometry import dot, union
from ..motif import Motif

APEX = (0.0, -13.0)  # the point of the slice
RADIUS = 26.0  # of the whole pizza, from the apex to the crust's outer edge
HALF_ANGLE = 28.0  # degrees either side of straight up
CRUST = 3.6  # depth of the crust band along the arc
GAP = 1.2  # standing line between crust and cheese
PEPPERONI = [(0.0, -4.0, 3.8), (-4.8, 3.2, 3.8), (4.6, 4.0, 3.8)]  # standing (u, v, diameter)
ROUND = 0.8  # blunts the point and the crust's corners
STEPS = 32


def _sector(radius):
    au, av = APEX
    a0, a1 = math.radians(90 - HALF_ANGLE), math.radians(90 + HALF_ANGLE)
    arc = [(au + radius * math.cos(a0 + (a1 - a0) * i / STEPS), av + radius * math.sin(a0 + (a1 - a0) * i / STEPS)) for i in range(STEPS + 1)]
    return Polygon([APEX, *arc])


def draw():
    whole = _sector(RADIUS).buffer(-ROUND, 16).buffer(ROUND, 16)
    cheese = _sector(RADIUS - CRUST - GAP).buffer(-ROUND, 16).buffer(ROUND, 16)
    crust = whole.difference(Point(*APEX).buffer(RADIUS - CRUST, 64))
    slice_ = union(cheese.difference(union(*(dot(*p) for p in PEPPERONI))), crust)
    return slice_


motif = Motif(name="pizza_slice", issue=113, draw=draw)
