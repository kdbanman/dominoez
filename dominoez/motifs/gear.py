"""A gear, face on: a solid disc with eight blunt trapezoid teeth and a
standing hub hole in the middle."""

import math

from shapely.geometry import Point, Polygon

from ..geometry import union
from ..motif import Motif

ROOT_R = 9.2  # radius of the disc the teeth stand on
TIP_R = 12.0  # radius at the teeth's tops
TEETH = 8
TOOTH_BASE = 30.0  # degrees of arc a tooth covers at the root
TOOTH_TIP = 19.0  # degrees of arc at the top, so each tooth is a trapezoid
HUB_D = 6.5  # standing hole
ROUND = 0.6  # blunts the teeth's corners


def _tooth(k):
    a = 360.0 * k / TEETH
    pts = []
    for r, half in ((ROOT_R - 0.5, TOOTH_BASE / 2), (TIP_R, TOOTH_TIP / 2)):
        for s in (1, -1):
            pts.append((r * math.cos(math.radians(a + s * half)), r * math.sin(math.radians(a + s * half))))
    return Polygon([pts[0], pts[2], pts[3], pts[1]])


def draw():
    gear = union(Point(0, 0).buffer(ROOT_R, 96), *(_tooth(k) for k in range(TEETH)))
    gear = gear.buffer(-ROUND, 16).buffer(ROUND, 16)
    return gear.difference(Point(0, 0).buffer(HUB_D / 2, 48))


motif = Motif(name="gear", issue=144, draw=draw)
