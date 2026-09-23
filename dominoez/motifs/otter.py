"""An otter floating on its back, seen from the front: a big round head
with two small round ears, two standing eye dots and a standing nose, on a
wide chest that ends at a wavy water line, with two standing paw ovals held
up together under the chin. The chest and the water line are one shape."""

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_C, HEAD_R = (0.0, 4.0), 6.5
EARS = [(-5.4, 8.4, 2.8), (5.4, 8.4, 2.8)]  # (u, v, diameter) small bumps on the top of the head
EYES = [(-2.3, 5.4, 2.0), (2.3, 5.4, 2.0)]  # standing (u, v, diameter)
NOSE = (0.0, 3.0, 2.4)  # standing
CHEST_C, CHEST_W, CHEST_H = (0.0, -4.0), 20.0, 12.0  # ellipse under the head, cut off below by the water
PAWS = [(-2.4, -3.2, 12.0), (2.4, -3.2, -12.0)]  # standing ovals (u, v, tilt in degrees), held up under the chin
PAW_W, PAW_H = 3.4, 5.2
WATER_SPAN = (-12.5, 12.5)  # u extent of the water line
WAVE_LEN, WAVE_AMP = 8.3, 0.8  # one full wave per WAVE_LEN mm
WAVE_V = -9.0  # centre line of the water; the chest ends here
WAVE_W = 2.2
ROUND = 0.5  # blunts tips
CLOSE = 0.8  # fills the creases where the ears and chest meet the head
SEAL = 0.6  # fills the standing slivers where the chest edge runs into the water line, narrower than the gap between the paws


def _ellipse(c, w, h, angle=0.0):
    e = affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)
    return affinity.rotate(e, angle, origin=c)


def _wave_points():
    u0, u1 = WATER_SPAN
    n = 64
    return [
        (u, WAVE_V + WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN))
        for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))
    ]


def draw():
    wave = _wave_points()
    above_water = Polygon(wave + [(WATER_SPAN[1], 30.0), (WATER_SPAN[0], 30.0)])
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    ears = union(*(dot(*e) for e in EARS))
    chest = _ellipse(CHEST_C, CHEST_W, CHEST_H).intersection(above_water)
    otter = union(head, ears, chest).buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    otter = union(otter, stroke(wave, WAVE_W)).buffer(SEAL, 16).buffer(-SEAL, 16)
    standing = union(*(dot(*e) for e in EYES), dot(*NOSE), *(_ellipse((u, v), PAW_W, PAW_H, a) for u, v, a in PAWS))
    return otter.difference(standing)


motif = Motif(name="otter", issue=79, draw=draw)
