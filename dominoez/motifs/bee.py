"""A cartoon bee, side on, flying left: a round head with one antenna and a
standing eye dot, sitting with a pinch directly against a fat striped
abdomen that carries one wing lobe on top and ends in a stinger."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_C, HEAD_R = (-8.0, -0.5), 3.2  # overlaps the front of the abdomen by a pinch
EYE = (-8.6, -0.3, 1.9)  # standing (u, v, diameter)
ANTENNA = [(-7.2, 2.8), (-8.6, 5.4)]  # up and forward from the top of the head
ANTENNA_W, ANTENNA_TIP = 1.6, 2.2
ABDOMEN_C, ABDOMEN_W, ABDOMEN_H = (3.0, 0.0), 15.0, 10.0  # the hero: fat and round
STINGER = [(10.0, 1.5), (10.0, -1.5), (12.8, 0.0)]  # at the back
STRIPES = [3.0, 6.8]  # u of each standing band across the abdomen, behind the wing's base
STRIPE_W = 1.5  # standing band width
STRIPE_LEN = 10.8  # just past the abdomen edges, so the bands cut clean through but stop short of the wing
WING_C, WING_W, WING_H, WING_ANGLE = (0.5, 7.5), 9.0, 5.0, 45.0  # one plump wing lobe standing on the front of the abdomen, sweeping up and back, clear of the head
ROUND = 0.5  # blunts tips and removes the slivers where a stripe crosses the abdomen edge
CLOSE = 0.5  # fills the creases where the wing and antenna meet, without bridging the wing to the head


def _ellipse(c, w, h, angle=0.0):
    e = affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)
    return affinity.rotate(e, angle, origin=c)


def _stripes():
    return union(*(stroke([(u, -STRIPE_LEN / 2), (u, STRIPE_LEN / 2)], STRIPE_W, cap="flat") for u in STRIPES))


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    abdomen = _ellipse(ABDOMEN_C, ABDOMEN_W, ABDOMEN_H)
    wing = _ellipse(WING_C, WING_W, WING_H, WING_ANGLE)
    antenna = union(stroke(ANTENNA, ANTENNA_W), dot(*ANTENNA[-1], ANTENNA_TIP))
    bee = union(head, abdomen, Polygon(STINGER), wing, antenna)
    bee = bee.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return bee.difference(union(_stripes(), dot(*EYE))).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="bee", issue=88, draw=draw)
