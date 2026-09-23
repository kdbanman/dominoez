"""A chubby helicopter seen from the side, facing right, tilted a little
nose-down as if pulling forward: a plump fuselage with one standing cockpit
window, a tapering tail boom ending in a fin, a short mast carrying the
rotor as one long bar, and a skid slung underneath."""

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_W, BODY_H, BODY_C = 15.0, 9.0, (0.5, 0.0)  # fuselage ellipse
WINDOW = (4.0, 0.8, 3.4)  # standing (u, v, diameter)
BOOM = [(-5.5, 0.5), (-12.5, 2.5)]  # tail boom centreline, root to tip
BOOM_W0, BOOM_W1 = 4.2, 2.6  # boom tapers toward the tail
FIN = [(-12.0, 2.5), (-11.0, 5.5)]  # tail fin rising from the boom tip
FIN_W = 2.6
MAST = [(1.0, 4.0), (1.0, 7.5)]
MAST_W = 2.6
ROTOR = [(-8.0, 8.5), (10.5, 8.5)]  # stops short of the fin, so no hole closes between them  # one long bar
ROTOR_W = 2.4
SKID = [(-6.0, -7.5), (6.0, -7.5)]
SKID_W = 2.2
LEGS = [[(-3.0, -3.5), (-3.5, -7.5)], [(4.0, -3.5), (4.5, -7.5)]]
LEG_W = 2.2
TILT = -8.0  # degrees, nose down
CLOSE = 1.0  # blends boom, mast and legs into the body
ROUND = 0.5


def _taper(a, b, w0, w1):
    (au, av), (bu, bv) = a, b
    du, dv = bu - au, bv - av
    n = math.hypot(du, dv)
    nu, nv = -dv / n, du / n
    body = Polygon([
        (au + nu * w0 / 2, av + nv * w0 / 2),
        (bu + nu * w1 / 2, bv + nv * w1 / 2),
        (bu - nu * w1 / 2, bv - nv * w1 / 2),
        (au - nu * w0 / 2, av - nv * w0 / 2),
    ])
    return union(body, dot(bu, bv, w1))


def draw():
    fuselage = affinity.scale(Point(*BODY_C).buffer(1.0, 64), BODY_W / 2, BODY_H / 2, origin=BODY_C)
    parts = union(
        fuselage,
        _taper(BOOM[0], BOOM[1], BOOM_W0, BOOM_W1),
        stroke(FIN, FIN_W),
        stroke(MAST, MAST_W),
        *(stroke(leg, LEG_W) for leg in LEGS),
        stroke(SKID, SKID_W),
    )
    parts = parts.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    heli = union(parts, stroke(ROTOR, ROTOR_W)).buffer(-ROUND, 16).buffer(ROUND, 16)
    heli = heli.difference(dot(*WINDOW))
    return affinity.rotate(heli, TILT, origin=(0, 0))


motif = Motif(name="helicopter", issue=103, draw=draw)
