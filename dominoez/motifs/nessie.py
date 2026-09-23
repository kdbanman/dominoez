"""Nessie: a gently waving water line with one big round hump rising out
of it, and a smooth thick S of neck rising from the hump's front to a
round head above, leaning slightly right, with a standing dot for the
eye."""

import math

from shapely.geometry import box

from ..geometry import dot, stroke, union
from ..motif import Motif

WATER_SPAN = (-12.5, 12.0)  # u extent of the water line, at v=0
WAVE_LEN, WAVE_AMP = 8.17, 0.5  # a gentle wave
WAVE_W = 2.2
HUMP_C, HUMP_D = (-5.0, 0.0), 13.0  # the hump is this disc centred on the water line, kept above it
NECK = [(0.5, 0.0), (6.0, 6.0), (-1.0, 10.0), (4.0, 14.0)]  # cubic Bezier: start on the hump's front, two controls, end at the skull; one smooth S
NECK_W = 5.2
HEAD = (5.0, 15.0, 7.0)  # (u, v, diameter)
EYE = (6.2, 15.6, 1.8)  # standing
CLOSE = 0.6  # blends the neck into the head and the hump into the water
ROUND = 0.5  # blunts the tips


def _water():
    u0, u1 = WATER_SPAN
    n = 64
    pts = [(u, WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN)) for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))]
    return stroke(pts, WAVE_W)


def _bezier(p0, p1, p2, p3, t):
    s = 1 - t
    return tuple(s**3 * a + 3 * s**2 * t * b + 3 * s * t**2 * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))


def _neck(n=48):
    return stroke([_bezier(*NECK, i / n) for i in range(n + 1)], NECK_W)


def draw():
    above_water = box(-30, 0.0, 30, 30)
    hump = dot(*HUMP_C, HUMP_D).intersection(above_water)
    nessie = union(_water(), hump, _neck().intersection(above_water), dot(*HEAD))
    nessie = nessie.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return nessie.difference(dot(*EYE))


motif = Motif(name="nessie", issue=95, draw=draw)
