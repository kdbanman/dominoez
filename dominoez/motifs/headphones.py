"""Over-ear headphones, front on: a fat headband arching over two big solid
ear cups that hang from its ends."""

import math

from shapely import affinity

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

BAND_C = (0.0, -2.0)  # centre of the headband arc
BAND_R = 9.5
BAND_W = 3.0
BAND_SPAN = (0.0, 180.0)  # degrees, right end round the top to the left end
CUP = (7.0, 9.5, 2.5)  # width, height, corner radius
CUP_C = (9.5, -5.5)  # right cup; the left is mirrored
CLOSE = 0.8  # fills the crease where each cup meets the band


def _arc():
    steps = 32
    a0, a1 = BAND_SPAN
    pts = [
        (BAND_C[0] + BAND_R * math.cos(math.radians(a)), BAND_C[1] + BAND_R * math.sin(math.radians(a)))
        for a in [a0 + (a1 - a0) * i / steps for i in range(steps + 1)]
    ]
    return stroke(pts, BAND_W)


def draw():
    cup = affinity.translate(rounded_rect(*CUP), *CUP_C)
    cups = [cup, affinity.scale(cup, -1.0, 1.0, origin=(0, 0))]
    return union(_arc(), *cups).buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="headphones", issue=37, draw=draw)
