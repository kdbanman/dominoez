"""A banana. A curved body that swells in the middle and tapers to a stem at
one end and a tip at the other, lying diagonally so it can be long."""

import math

from shapely import affinity
from shapely.geometry import Point

from ..geometry import stroke, union
from ..motif import Motif

RADIUS = 16.0  # of the arc the banana follows
SWEEP = 100.0  # degrees of arc
WIDTH = 10.0  # at the fattest point
END_WIDTH = 2.6  # at the tapered ends, above the channel minimum
STEM = 2.5  # length of the stem past the end of the body
TILT = -40.0  # degrees; hang the banana across the face


def _arc(t: float) -> tuple[float, float]:
    a = math.radians(-90 - SWEEP / 2 + SWEEP * t)
    return (RADIUS * math.cos(a), RADIUS * math.sin(a) + RADIUS)


def draw():
    # Sweep a circle along the arc, swelling in the middle: a smooth tapered body.
    discs = []
    for i in range(121):
        t = i / 120
        w = END_WIDTH + (WIDTH - END_WIDTH) * math.sin(math.pi * t) ** 0.8
        discs.append(Point(*_arc(t)).buffer(w / 2, 24))
    body = union(*discs)
    # The stem continues the arc's tangent past the start of the body.
    x0, y0 = _arc(0)
    x1, y1 = _arc(0.02)
    dx, dy = x0 - x1, y0 - y1
    n = math.hypot(dx, dy)
    stem = stroke([(x0, y0), (x0 + STEM * dx / n, y0 + STEM * dy / n)], END_WIDTH, cap="flat")
    banana = union(body, stem)
    return affinity.rotate(banana, TILT, origin=(0, 0))


motif = Motif(name="banana", issue=19, draw=draw)
