"""A cartoon hedgehog, side on, walking right: a fat oval body whose whole
back is a zigzag of spines, a pointed snout at the front, and two little
nub legs. The eye is a standing dot."""

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (-1.0, 0.0), 22.0, 13.0  # ellipse axes of the body under the spines
SPINE_ARC = (170.0, 25.0)  # degrees around the ellipse the zigzag covers, back to front
SPINES = 8  # number of spikes along the arc
SPINE_OUT = 1.5  # spike tips this far out along the ellipse radius; valleys sit on the ellipse
SNOUT = [(6.0, 3.0), (12.8, -1.5), (7.0, -4.5)]  # pointed snout at the front
EYE = (7.5, 0.8, 2.0)  # standing (u, v, diameter)
LEGS = [[(-6.0, -5.0), (-6.0, -6.8)], [(4.0, -5.0), (4.0, -6.8)]]  # little nub legs, just proud of the belly
LEG_W = 3.2
ROUND = 0.6  # blunts the spike and snout tips
CLOSE = 0.7  # rounds the valleys between spikes past the wall minimum and fills creases


def _ellipse(c, w, h):
    return affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def _spines():
    """Zigzag polygon riding the top of the body ellipse."""
    a0, a1 = SPINE_ARC
    cu, cv = BODY_C
    n = 2 * SPINES
    points = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        k = SPINE_OUT if i % 2 == 1 else 1.0
        points.append((cu + k * BODY_W / 2 * math.cos(a), cv + k * BODY_H / 2 * math.sin(a)))
    points.append((cu, cv))
    return Polygon(points)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    legs = union(*(stroke(l, LEG_W) for l in LEGS))
    hedgehog = union(body, _spines(), Polygon(SNOUT), legs)
    hedgehog = hedgehog.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return hedgehog.difference(dot(*EYE))


motif = Motif(name="hedgehog", issue=86, draw=draw)
