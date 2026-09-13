"""Chunky over-ear headphones, front on, like the emoji: a thick smooth
headband arching over two big plump ear cups that hang from its ends. The
band's outer edge runs straight into the outer edge of each cup, and each
cup carries a small standing dot for the driver."""

import math

from shapely import affinity

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

CUP_W, CUP_H, CUP_R = 7.6, 9.4, 2.4  # plump rounded rectangle
CUP_C = (7.4, -4.6)  # right cup; the left is mirrored
BAND_W = 3.4
BAND_R = CUP_C[0] + CUP_W / 2 - BAND_W / 2  # centreline radius, so the band's outer edge meets the cup's outer edge
BAND_C = (0.0, -2.0)  # centre of the headband arc, a little below the cup tops so the ends sit inside the cups
BAND_SPAN = (0.0, 180.0)  # degrees, right end over the top to the left end; the ends drop vertically into the cups
DRIVER = (7.4, -4.9, 2.6)  # standing (u, v, diameter) on the right cup; the left is mirrored
CLOSE = 1.2  # blends the band into the top of each cup


def _arc():
    steps = 64
    a0, a1 = BAND_SPAN
    pts = [
        (BAND_C[0] + BAND_R * math.cos(math.radians(a)), BAND_C[1] + BAND_R * math.sin(math.radians(a)))
        for a in [a0 + (a1 - a0) * i / steps for i in range(steps + 1)]
    ]
    return stroke(pts, BAND_W)


def _mirror(g):
    return affinity.scale(g, -1.0, 1.0, origin=(0, 0))


def draw():
    cup = affinity.translate(rounded_rect(CUP_W, CUP_H, CUP_R), *CUP_C)
    driver = dot(*DRIVER)
    phones = union(_arc(), cup, _mirror(cup)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return phones.difference(union(driver, _mirror(driver)))


motif = Motif(name="headphones", issue=37, draw=draw)
