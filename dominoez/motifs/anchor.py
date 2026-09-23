"""A classic anchor, upright, nothing else: a ring at the top standing
as a hole in a cut collar, a shank down the middle that thickens toward
the bottom, a stock bar with knobbed ends across the shank under the
ring, and two heavy arms curving up and out from the crown into fat
arrowhead flukes. Laid out big, then scaled to fit."""

import math

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

RING_C, RING_D, RING_HOLE = (0.0, 10.8), 6.8, 2.8  # cut collar and its standing hole
SHANK = [(0.0, 8.5), (0.0, -7.5)]
SHANK_W0, SHANK_W1 = 2.8, 3.8  # light at the ring, heavier at the crown
STOCK = [(-7.0, 6.8), (7.0, 6.8)]
STOCK_W = 2.8
STOCK_END_D = 3.6  # knobs on the stock ends
ARM_C, ARM_R = (0.0, 0.5), 9.0  # the arms follow this arc; the crown is its bottom
ARM_SWEEP = (200.0, 340.0)  # degrees of arc from the left fluke round the bottom to the right fluke
ARM_W0, ARM_W1 = 3.2, 5.0  # thin near the crown, heavy toward the flukes
FLUKE = [(-3.4, -0.8), (3.2, 0.4), (0.4, 5.4)]  # arrowhead blade relative to the right arm's end; mirrored for the left
ROUND = 0.55  # blunts the fluke tips
CLOSE = 0.8  # blends arms into the shank
SCALE = 0.97


def _taper(points, w0, w1, n=24):
    """A path buffered with a width that eases from w0 at the start to w1 at the end."""
    ls = LineString(points)
    discs = []
    for i in range(n + 1):
        t = i / n
        p = ls.interpolate(t, normalized=True)
        discs.append(Point(p.x, p.y).buffer((w0 + (w1 - w0) * t) / 2, 24))
    return union(*(union(discs[i], discs[i + 1]).convex_hull for i in range(n)))


def _arc(a0, a1, n=24):
    cu, cv = ARM_C
    return [(cu + ARM_R * math.cos(math.radians(a0 + (a1 - a0) * i / n)), cv + ARM_R * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]


def _fluke(end, mirror):
    eu, ev = end
    return Polygon([((-du if mirror else du) + eu, dv + ev) for du, dv in FLUKE])


def draw():
    a0, a1 = ARM_SWEEP
    mid = (a0 + a1) / 2
    left, right = _arc(mid, a0), _arc(mid, a1)
    arms = union(_taper(left, ARM_W0, ARM_W1), _taper(right, ARM_W0, ARM_W1))
    flukes = union(_fluke(left[-1], True), _fluke(right[-1], False))
    stock = union(stroke(STOCK, STOCK_W), dot(*STOCK[0], STOCK_END_D), dot(*STOCK[1], STOCK_END_D))
    body = union(dot(*RING_C, RING_D), _taper(SHANK, SHANK_W0, SHANK_W1), stock, arms, flukes)
    body = body.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(body.difference(dot(*RING_C, RING_HOLE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="anchor", issue=97, draw=draw)
