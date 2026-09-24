"""A cartoon submarine, side on, heading right, under a wavy water line:
a long fat capsule of a hull with three standing portholes, a conning
tower on top with a periscope rising through the surface to a short head
turned forward, a tail fin on the stern and a propeller behind it."""

import math

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

HULL_C, HULL_W, HULL_H = (1.0, -3.0), 18.5, 7.8  # capsule hull
PORTHOLES = [(-3.0, -3.0, 2.3), (2.0, -3.0, 2.3), (7.0, -3.0, 2.3)]  # standing (u, v, diameter)
TOWER_C, TOWER_W, TOWER_H = (-1.5, 1.2), 6.5, 4.6  # conning tower sitting on the hull
PERISCOPE = [(-0.5, 2.5), (-0.5, 9.6), (2.2, 9.6)]  # up through the water, then turned forward
PERISCOPE_W = 2.0
FIN = [(-7.0, 0.0), (-10.0, 3.2), (-10.0, -0.5)]  # tail fin on the stern, root inside the hull
PROP_C, PROP_W, PROP_H = (-11.1, -3.0), 2.2, 6.4  # propeller blades as one rounded bar behind the stern
PROP_HUB = [(-8.0, -3.0), (-10.5, -3.0)]
PROP_HUB_W = 2.4
WATER_SPAN = (-11.5, 11.5)
WAVE_LEN, WAVE_AMP = 8.33, 0.8
WAVE_V = 6.4  # the surface, above the tower
WAVE_W = 2.0
ROUND = 0.55
CLOSE = 0.8


def draw():
    hull = affinity.translate(rounded_rect(HULL_W, HULL_H, HULL_H / 2), *HULL_C)
    tower = affinity.translate(rounded_rect(TOWER_W, TOWER_H, 1.2), *TOWER_C)
    periscope = stroke(PERISCOPE, PERISCOPE_W)
    fin = Polygon(FIN)
    prop = union(stroke(PROP_HUB, PROP_HUB_W), affinity.translate(rounded_rect(PROP_W, PROP_H, 1.0), *PROP_C))
    sub = union(hull, tower, periscope, fin, prop)
    sub = sub.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    sub = sub.difference(union(*(dot(u, v, d) for u, v, d in PORTHOLES)))
    u0, u1 = WATER_SPAN
    n = 64
    pts = [(u, WAVE_V + WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN)) for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))]
    return union(sub, stroke(pts, WAVE_W))


motif = Motif(name="submarine", issue=100, draw=draw)
