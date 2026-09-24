"""The peace sign: a fat ring with a vertical bar down its middle and two
arms forking from the centre down to the lower left and lower right,
all one stroke weight."""

import math

from shapely.geometry import Point

from ..geometry import stroke, union
from ..motif import Motif

OUTER_D = 25.0  # mm outer diameter of the ring
WEIGHT = 3.4  # mm stroke width of the ring and the fork
FORK_ANGLES = [90.0, 225.0, 315.0]  # degrees from the centre to where each arm meets the ring: up, lower left, lower right
CLOSE = 0.6  # smooths the joins where the arms meet the ring and each other


def draw():
    ring_r = OUTER_D / 2 - WEIGHT / 2  # centreline radius
    ring = Point(0, 0).buffer(ring_r + WEIGHT / 2, 96).difference(Point(0, 0).buffer(ring_r - WEIGHT / 2, 96))
    arms = [stroke([(0, 0), (ring_r * math.cos(math.radians(a)), ring_r * math.sin(math.radians(a)))], WEIGHT) for a in FORK_ANGLES]
    sign = union(ring, *arms)
    return sign.buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="peace_sign", issue=160, draw=draw)
