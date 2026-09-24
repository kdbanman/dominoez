"""The classic T. rex icon, side on, facing right: one S-curve runs from
a thick tail out the back, through a fat body leaning forward, up a short
neck to one huge smooth head with the mouth closed. Two big legs on fat
feet carry it and one tiny arm pokes out of the chest. The eye is a
standing dot. Laid out big, then scaled to fit."""

from shapely import affinity
from shapely.geometry import LineString, Point

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

CURVE = [(-12.5, 2.5), (-8.5, 0.0), (-3.0, -1.5), (3.0, 1.0), (6.0, 6.0)]  # tail tip to neck, the S
CURVE_W0, CURVE_W1 = 2.6, 6.0  # thin at the tail tip, thick at the neck
BODY_C, BODY_W, BODY_H, BODY_TILT = (-1.0, -1.0), 12.0, 9.0, 20.0  # fat body leaning forward
HEAD_C, HEAD_D = (8.5, 10.0), 10.5  # skull disc
SNOUT_C, SNOUT_W, SNOUT_H = (11.5, 9.2), 8.5, 7.0  # rounded box that carries the snout forward, one mass with the skull
EYE = (9.4, 12.2, 2.2)  # standing (u, v, diameter)
ARM = [(5.5, 1.5), (9.0, 0.5)]  # tiny arm out of the chest
ARM_W = 2.4
LEGS = [[(-3.0, -3.0), (-3.5, -9.0)], [(4.0, -3.0), (4.5, -9.0)]]  # hip to ankle
LEG_W = 5.0
FEET = [[(-5.0, -10.0), (-1.0, -10.0)], [(3.5, -10.0), (8.0, -10.0)]]  # toes forward
FOOT_W = 3.0
ROUND = 0.55  # blunts the tail tip, teeth and toes
CLOSE = 0.8  # blends neck, legs and tail into the body
SCALE = 0.8


def _ellipse(c, w, h, tilt=0.0):
    e = affinity.scale(Point(c).buffer(1.0, 64), w / 2, h / 2, origin=c)
    return affinity.rotate(e, tilt, origin=c)


def _taper(points, w0, w1, n=32):
    """A path buffered with a width that eases from w0 at the start to w1 at the end."""
    ls = LineString(points)
    discs = []
    for i in range(n + 1):
        t = i / n
        p = ls.interpolate(t, normalized=True)
        discs.append(Point(p.x, p.y).buffer((w0 + (w1 - w0) * t) / 2, 24))
    return union(*(union(discs[i], discs[i + 1]).convex_hull for i in range(n)))


def draw():
    curve = _taper(CURVE, CURVE_W0, CURVE_W1)
    body = _ellipse(BODY_C, BODY_W, BODY_H, BODY_TILT)
    head = union(dot(*HEAD_C, HEAD_D), affinity.translate(rounded_rect(SNOUT_W, SNOUT_H, 2.5), *SNOUT_C))
    limbs = union(stroke(ARM, ARM_W), *(stroke(leg, LEG_W) for leg in LEGS), *(stroke(foot, FOOT_W) for foot in FEET))
    rex = union(curve, body, head, limbs)
    rex = rex.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(rex.difference(dot(*EYE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="t_rex", issue=91, draw=draw)
