"""A stegosaurus, side on, facing right, as one silhouette: a plump
round-bellied blob of a body with three big blunt triangular plates
standing on its back, a small round head held low on a short neck, a
thick tail sweeping down and back, and two stubby nub legs just proud of
the belly. The eye is a standing dot. Laid out
big, then scaled to fit."""

import math

from shapely import affinity
from shapely.geometry import LineString, Point

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (0.0, -0.5), 18.0, 13.5  # the plump belly
PLATE_U = [-6.0, 0.0, 6.0]  # plates along the back; their bases follow the arch
PLATE_H, PLATE_BASE, PLATE_TIP = 6.0, 5.6, 1.8  # big blunt triangles
PLATE_LEAN = -0.6  # tips lean back a little
PLATE_SINK = 2.0  # how far each base sits inside the body
NECK = [(7.5, -2.0), (11.0, -4.0)]
NECK_W = 5.0
HEAD = (12.0, -4.3, 5.8)  # (u, v, diameter)
EYE = (12.3, -3.6, 1.9)  # standing
TAIL = [(-7.0, -2.0), (-11.5, -3.5), (-14.0, -7.0)]
TAIL_W0, TAIL_W1 = 6.5, 2.8
LEGS = [[(-4.5, -5.0), (-4.5, -8.0)], [(4.5, -5.0), (4.5, -8.0)]]  # stubby nubs just proud of the belly, each a pair seen edge on
LEG_W = 4.6
ROUND = 0.55  # blunts plate tips and the tail tip
CLOSE = 0.8  # blends neck, legs and tail into the body
SCALE = 0.88


def _ellipse(c, w, h):
    return affinity.scale(Point(c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def _taper(points, w0, w1, n=24):
    """A path buffered with a width that eases from w0 at the start to w1 at the end."""
    ls = LineString(points)
    discs = []
    for i in range(n + 1):
        t = i / n
        p = ls.interpolate(t, normalized=True)
        discs.append(Point(p.x, p.y).buffer((w0 + (w1 - w0) * t) / 2, 24))
    return union(*(union(discs[i], discs[i + 1]).convex_hull for i in range(n)))


def _plate(u):
    cu, cv = BODY_C
    arch = cv + BODY_H / 2 * math.sqrt(max(0.0, 1 - (2 * (u - cu) / BODY_W) ** 2))
    base = (u, arch - PLATE_SINK)
    return _taper([base, (u + PLATE_LEAN, base[1] + PLATE_H)], PLATE_BASE, PLATE_TIP, n=4)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    plates = union(*(_plate(u) for u in PLATE_U))
    head = union(stroke(NECK, NECK_W), dot(*HEAD))
    tail = _taper(TAIL, TAIL_W0, TAIL_W1)
    legs = union(*(stroke(leg, LEG_W) for leg in LEGS))
    steg = union(body, plates, head, tail, legs)
    steg = steg.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(steg.difference(dot(*EYE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="stegosaurus", issue=92, draw=draw)
