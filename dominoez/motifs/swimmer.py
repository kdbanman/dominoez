"""A swimmer doing front crawl, seen from the side and heading right: a
wavy water line, a round head lifted above it, a long low back rising out
of the water behind the head, and one bent arm swinging up from the
shoulder, over the head, and forward to the next stroke."""

import math

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

WATER_SPAN = (-9.0, 11.5)  # u extent of the water line
WAVE_LEN, WAVE_AMP = 14.0, 0.7  # one full wave per WAVE_LEN mm
WAVE_PHASE = 7.5  # u of a rising zero crossing, chosen to put a trough under the head
WAVE_W = 1.8
HEAD = (4.5, 4.5, 4.6)  # (u, v, diameter), well clear of the trough below it
BACK_W, BACK_H = 9.0, 3.0  # ellipse axes of the back, merging with the water
BACK_C = (-3.0, 0.8)
ARM = [(-2.5, 2.0), (-0.5, 6.5), (2.0, 10.0), (7.0, 9.0), (10.0, 5.5)]  # shoulder, elbow, hand; a wall past the minimum from the head
ARM_W = 2.6
CLOSE = 0.5  # rounds the crease where the back and arm leave the water


def _water():
    u0, u1 = WATER_SPAN
    n = 48
    points = []
    for i in range(n + 1):
        u = u0 + (u1 - u0) * i / n
        points.append((u, WAVE_AMP * math.sin(2 * math.pi * (u - WAVE_PHASE) / WAVE_LEN)))
    return stroke(points, WAVE_W)


def draw():
    back = affinity.scale(Point(*BACK_C).buffer(1.0, 64), BACK_W / 2, BACK_H / 2, origin=BACK_C)
    swimmer = union(_water(), back, stroke(ARM, ARM_W), dot(*HEAD))
    return swimmer.buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="swimmer", issue=45, draw=draw)
