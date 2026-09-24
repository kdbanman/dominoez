"""A snail, side on, crawling left, drawn like the classic silhouette: a
big round shell sitting on the back of a long low foot, the foot rising at
the front into a round head, and two thin eye stalks with blob tips
reaching up from the head. A standing spiral inside the shell reads as the
whorl."""

import math

from shapely.geometry import LineString, Point, Polygon

from ..geometry import stroke, union
from ..motif import Motif

SHELL_C = (3.5, 2.0)  # centre of the shell disc
SHELL_R = 8.2
SPIRAL_TURNS = 1.6  # standing spiral inside the shell
SPIRAL_W = 1.7  # wide enough to stand as an island
SPIRAL_R0, SPIRAL_R1 = 1.4, 6.3  # the spiral runs from this inner radius out to this outer one, clear of the rim
FOOT = [  # the body: a long low foot, pointed tail at the right, blunt front at the left
    (12.0, -5.6),
    (6.0, -3.4),
    (-4.0, -3.2),
    (-10.0, -3.8),
    (-12.4, -5.0),
    (-11.0, -6.6),
    (4.0, -6.6),
]
NECK = [(-9.2, -4.4), (-10.9, -0.6), (-10.4, 2.8)]  # curves up from the front of the foot to the head
NECK_W = 5.0
HEAD = (-10.4, 3.4, 6.4)  # round head at the front of the rise (u, v, diameter)
STALKS = [[(-11.6, 5.6), (-13.4, 11.4)], [(-9.2, 6.0), (-8.2, 12.0)]]  # two eye stalks in a V
STALK_W = 1.7
TIP_D = 2.6  # blob at the end of each stalk
CLOSE = 0.8  # blends the head and stalks into the foot
ROUND = 0.5  # blunts the tail tip and the tips of the blobs


def _spiral():
    n = 160
    pts = []
    for i in range(n + 1):
        t = i / n
        a = 2 * math.pi * SPIRAL_TURNS * t
        r = SPIRAL_R0 + (SPIRAL_R1 - SPIRAL_R0) * t
        pts.append((SHELL_C[0] + r * math.cos(a), SHELL_C[1] + r * math.sin(a)))
    return LineString(pts).buffer(SPIRAL_W / 2, 8)


def draw():
    shell = Point(*SHELL_C).buffer(SHELL_R, 96)
    body = union(Polygon(FOOT), stroke(NECK, NECK_W), Point(HEAD[0], HEAD[1]).buffer(HEAD[2] / 2, 32))
    stalks = union(*(stroke(s, STALK_W) for s in STALKS), *(Point(*s[-1]).buffer(TIP_D / 2, 24) for s in STALKS))
    snail = union(shell, body, stalks).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return snail.difference(_spiral()).buffer(-ROUND, 16).buffer(ROUND, 16)  # the last opening clears the sliver where the spiral leaves the rim


motif = Motif(name="snail", issue=83, draw=draw)
