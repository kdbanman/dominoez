"""A medal: two fat ribbon straps hanging in a V, crossing just above a
round disc, and a standing five-pointed star on the disc."""

import math

from shapely.geometry import Point, Polygon

from ..geometry import union
from ..motif import Motif

DISC_C = (0.0, -5.8)
DISC_R = 8.5
STAR_R = (6.3, 2.9)  # outer and inner radius of the standing star, point up
STAR_ROUND = 0.9  # blunts the star's points past the island minimum
STRAP = [(-10.8, 13.2), (-5.2, 13.2), (2.6, 2.4), (-3.0, 2.4)]  # left strap, flat top; the right is its mirror
CLOSE = 0.8  # fills the creases where the straps meet the disc and each other
ROUND = 0.6  # blunts the straps' top corners


def _star():
    pts = []
    for k in range(10):
        r = STAR_R[k % 2]
        a = math.radians(90 + 36 * k)
        pts.append((DISC_C[0] + r * math.cos(a), DISC_C[1] + r * math.sin(a)))
    return Polygon(pts).buffer(-STAR_ROUND, 16).buffer(STAR_ROUND, 16)


def draw():
    disc = Point(*DISC_C).buffer(DISC_R, 96)
    left = Polygon(STRAP)
    right = Polygon([(-u, v) for u, v in STRAP])
    medal = union(disc, left, right).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return medal.difference(_star())


motif = Motif(name="medal", issue=138, draw=draw)
