"""A cute penguin, front-on: a round head on a tall egg body, two flippers
held out and down, and two flat feet. The belly is a standing oval, so the
black back wraps around it, and the eyes and a small beak are standing."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (0.0, -2.8), 13.5, 18.0  # tall egg body
HEAD_C, HEAD_R = (0.0, 7.8), 5.2  # round head, pinched at the neck
BELLY_C, BELLY_W, BELLY_H = (0.0, -3.2), 7.5, 12.0  # standing oval inside the body
EYES = [(-2.2, 9.5, 2.0), (2.2, 9.5, 2.0)]  # standing (u, v, diameter)
BEAK = [(-2.2, 7.3), (2.2, 7.3), (0.0, 4.5)]  # standing wedge under the eyes
FLIPPERS = [[(-5.2, 3.0), (-11.0, -5.0)], [(5.2, 3.0), (11.0, -5.0)]]  # out and down from the shoulders
FLIPPER_W = 3.4
FEET = [(-3.0, -12.4), (3.0, -12.4)]  # centres of the flat feet
FOOT_W, FOOT_H = 5.0, 2.4
BEAK_ROUND = 0.8  # blunts the beak so it stays past the island minimum
ROUND = 0.5  # blunts tips
CLOSE = 1.0  # fills the creases at the neck and shoulders


def _ellipse(c, w, h):
    return affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    flippers = union(*(stroke(f, FLIPPER_W) for f in FLIPPERS))
    feet = union(*(_ellipse(c, FOOT_W, FOOT_H) for c in FEET))
    penguin = union(body, head, flippers, feet)
    penguin = penguin.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    beak = Polygon(BEAK).buffer(-BEAK_ROUND, 16).buffer(BEAK_ROUND, 16)
    standing = union(_ellipse(BELLY_C, BELLY_W, BELLY_H), *(dot(*e) for e in EYES), beak)
    return penguin.difference(standing)


motif = Motif(name="penguin", issue=80, draw=draw)
