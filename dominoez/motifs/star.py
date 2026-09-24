"""A fat five-pointed star, one point straight up, drawn as a solid
silhouette with the tips blunted and the inside corners softened."""

import math

from shapely.geometry import Polygon

from ..motif import Motif

OUTER_R = 13.2  # mm from the centre to a tip, before the tips are blunted; the star spans about 24.5 mm
INNER_R = 6.6  # mm from the centre to an inside corner; half the outer radius makes a fat star
ROUND = 0.9  # blunts the five tips
CLOSE = 0.7  # softens the five inside corners


def _outline():
    pts = []
    for i in range(10):
        a = math.pi / 2 + i * math.pi / 5  # start at the top tip, go counter-clockwise
        r = OUTER_R if i % 2 == 0 else INNER_R
        pts.append((r * math.cos(a), r * math.sin(a)))
    return pts


def draw():
    star = Polygon(_outline())
    return star.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="star", issue=158, draw=draw)
