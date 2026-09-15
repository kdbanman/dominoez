"""The swimming pictogram, as on a pool sign, heading right: a round head
at the front, just above the water, a horizontal rounded bar for the body
lying along the surface behind it, and one arm rising from the shoulder
mid-stroke, bent at the elbow with the forearm reaching forward over the
head. Beneath it all, a wavy water line of three smooth waves, a little
wider than the swimmer."""

import math

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif
from shapely import affinity

HEAD = (9.0, 3.6, 5.8)  # (u, v, diameter); front of the swimmer, a wall clear of the body and arm
BODY_W, BODY_H = 14.0, 3.2  # rounded bar lying along the water
BODY_C = (-2.0, 1.6)
ARM = [(3.0, 2.0), (0.0, 10.2), (10.8, 9.0)]  # shoulder just behind the head end of the body, elbow up and back, hand forward over the head
ARM_W = 2.6
WATER_SPAN = (-10.5, 12.5)  # u extent of the water line
WAVE_LEN, WAVE_AMP = 7.67, 0.9  # one full wave per WAVE_LEN mm
WAVE_V = -3.4  # centre line of the water, a wall below the body
WAVE_W = 2.0
CLOSE = 0.9  # blends the shoulder into the body and the elbow into one smooth bend


def _water():
    u0, u1 = WATER_SPAN
    n = 64
    points = [
        (u, WAVE_V + WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN))
        for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))
    ]
    return stroke(points, WAVE_W)


def draw():
    body = affinity.translate(rounded_rect(BODY_W, BODY_H, BODY_H / 2), *BODY_C)
    figure = union(body, stroke(ARM, ARM_W))
    figure = figure.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(figure, dot(*HEAD), _water())


motif = Motif(name="swimmer", issue=45, draw=draw)
