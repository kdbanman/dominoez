"""A trophy cup: a tall cup flaring to a lip at the top, a fat C-shaped
handle on each side, a short stem and a two-step base."""

import math

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

# The right half of the cup's outline, (u, v), from the bottom centre up to the lip; the left is its mirror.
CUP = [(0.0, 0.0), (3.2, 0.4), (5.2, 2.6), (6.3, 6.5), (6.9, 10.5), (7.2, 14.5)]
LIP = (16.0, 2.8, 1.0)  # rim band across the cup's top: width, height, corner radius
LIP_C = (0.0, 14.6)
HANDLE_C = (7.0, 8.0)  # centre of the right handle's arc; the left is mirrored
HANDLE_R = 3.9  # arc radius of the handle's centreline
HANDLE_W = 2.8
HANDLE_STEPS = 12  # points along the half circle
STEM = [(0.0, 0.5), (0.0, -4.5)]
STEM_W = 4.2
COLLAR = (8.0, 2.4, 0.8)  # small plate under the stem
COLLAR_C = (0.0, -4.8)
BASE = (14.5, 3.4, 1.0)  # the foot plate
BASE_C = (0.0, -7.5)
CLOSE = 1.0  # rounds the cup's bottom and fills the crease where the handles meet the cup
ROUND = 0.5


def _handle(sign):
    pts = []
    for i in range(HANDLE_STEPS + 1):
        a = math.pi / 2 - math.pi * i / HANDLE_STEPS  # from the top of the arc round the outside to the bottom
        pts.append((sign * (HANDLE_C[0] + HANDLE_R * math.cos(a)), HANDLE_C[1] + HANDLE_R * math.sin(a)))
    return stroke(pts, HANDLE_W)


def draw():
    cup = Polygon(CUP + [(-u, v) for u, v in reversed(CUP[1:])])
    lip = affinity.translate(rounded_rect(*LIP), *LIP_C)
    stem = stroke(STEM, STEM_W)
    collar = affinity.translate(rounded_rect(*COLLAR), *COLLAR_C)
    base = affinity.translate(rounded_rect(*BASE), *BASE_C)
    trophy = union(cup, lip, _handle(1), _handle(-1), stem, collar, base)
    return trophy.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="trophy", issue=135, draw=draw)
