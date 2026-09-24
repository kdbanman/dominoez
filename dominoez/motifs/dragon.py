"""A cartoon dragon, side on, facing right, built on one S-curve: a fat
tail curling away at the lower left and ending in a spade, a big round
body, and a thick neck rising to a snouted head at the upper right with
one puff of smoke in front of the nose. One big scalloped bat wing rises
from the back and two chubby legs hang under the body. The eye is a
standing dot. Laid out big, then scaled to fit."""

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

CURVE = [(-13.5, -1.0), (-12.5, -5.5), (-8.0, -7.0), (-2.0, -5.0), (4.0, -1.0), (6.5, 4.0), (7.0, 9.0)]  # tail tip to skull, the S
CURVE_W0, CURVE_W1 = 2.2, 5.6  # thin at the tail tip, thick at the neck
BODY_C, BODY_W, BODY_H = (-0.5, -1.5), 14.0, 11.0  # the body mass hung on the curve
SPADE = [(-16.0, 1.0), (-11.0, 1.0), (-13.5, 5.0)]  # the tail's spade tip
HEAD_C, HEAD_D = (7.0, 10.5), 7.0  # skull
SNOUT_C, SNOUT_W, SNOUT_H = (10.5, 9.6), 7.0, 4.4  # rounded box carrying the snout forward
EYE = (7.6, 11.2, 2.1)  # standing
SMOKE = (14.6, 14.2, 2.8)  # one cut puff in front of and above the nose (u, v, diameter)
WING = [(1.0, 2.5), (-2.0, 15.5), (-5.5, 11.5), (-9.5, 14.0), (-10.5, 9.0), (-14.0, 8.5), (-7.0, 1.0)]  # one bat wing fanning up from the back, two scallops between three finger tips; root inside the body
LEGS = [((-5.0, -4.0), (-5.0, -9.5)), ((3.5, -4.0), (3.5, -9.5))]  # hip to ankle
LEG_W = 4.0
FEET = [[(-5.6, -10.0), (-2.8, -10.0)], [(2.9, -10.0), (5.9, -10.0)]]  # toes forward
FOOT_W = 2.8
ROUND = 0.55  # blunts the spade, wing tips and toes
CLOSE = 0.8  # blends the parts into one body
SCALE = 0.78


def _ellipse(c, w, h):
    return affinity.scale(Point(c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def _taper(points, w0, w1, n=48):
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
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    head = union(dot(*HEAD_C, HEAD_D), affinity.translate(rounded_rect(SNOUT_W, SNOUT_H, 1.8), *SNOUT_C))
    legs = union(*(stroke([a, b], LEG_W) for a, b in LEGS), *(stroke(f, FOOT_W) for f in FEET))
    dragon = union(curve, body, Polygon(SPADE), head, Polygon(WING), legs)
    dragon = dragon.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(union(dragon.difference(dot(*EYE)), dot(*SMOKE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="dragon", issue=94, draw=draw)
