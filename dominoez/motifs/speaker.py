"""A loudspeaker icon facing right: a driver box, a flared cone, and three
sound arcs rippling away from it."""

import math

from shapely.geometry import Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

DRIVER = (-11.0, -3.5, -6.5, 3.5)
CONE = [(-8.0, -3.5), (-6.5, -3.5), (-1.5, -9.0), (-1.5, 9.0), (-6.5, 3.5), (-8.0, 3.5)]  # its tail hides in the driver
TIP = 0.6  # rounds the cone's sharp tips, past half the channel minimum
ARC_C = (-1.0, 0.0)
ARC_RADII = [5.0, 8.5, 12.0]  # walls of 1.7 between neighbours
ARC_W = 1.8
ARC_SPAN = 50.0  # degrees either side of straight ahead
CORNER = 0.8


def _arc(r):
    steps = 24
    pts = [
        (ARC_C[0] + r * math.cos(math.radians(a)), ARC_C[1] + r * math.sin(math.radians(a)))
        for a in [-ARC_SPAN + 2 * ARC_SPAN * i / steps for i in range(steps + 1)]
    ]
    return stroke(pts, ARC_W)


def draw():
    driver = box(*DRIVER).buffer(-CORNER, 8).buffer(CORNER, 8)
    cone = Polygon(CONE).buffer(-TIP, 8).buffer(TIP, 8)
    return union(driver, cone, *(_arc(r) for r in ARC_RADII))


motif = Motif(name="speaker", issue=16, draw=draw)
