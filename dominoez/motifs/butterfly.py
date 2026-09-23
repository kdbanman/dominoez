"""A butterfly, top-down, head up: a slim body with a round head and two
antennae, and on each side a big upper wing lobe and a smaller lower lobe,
each carrying a standing spot. Symmetric about the centreline."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (0.0, -1.0), 3.6, 15.0
HEAD_C, HEAD_R = (0.0, 7.0), 2.0
ANTENNAE = [[(-1.0, 8.5), (-3.5, 12.0)], [(1.0, 8.5), (3.5, 12.0)]]
ANTENNA_W, ANTENNA_TIP = 1.5, 2.2
UPPER_C, UPPER_W, UPPER_H, UPPER_ANGLE = (7.0, 3.0), 13.0, 9.0, 25.0  # right upper wing lobe; mirrored for the left
LOWER_C, LOWER_W, LOWER_H, LOWER_ANGLE = (5.5, -5.0), 9.0, 7.0, -15.0  # right lower wing lobe
SPOTS = [(8.0, 4.0, 2.8), (5.8, -5.5, 2.2)]  # standing (u, v, diameter) on the right; mirrored
ROUND = 0.5  # blunts tips
CLOSE = 0.9  # fills the creases where the wings meet the body


def _ellipse(c, w, h, angle=0.0):
    e = affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)
    return affinity.rotate(e, angle, origin=c)


def _both(g):
    return union(g, affinity.scale(g, -1.0, 1.0, origin=(0, 0)))


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    antennae = union(*(union(stroke(a, ANTENNA_W), dot(*a[-1], ANTENNA_TIP)) for a in ANTENNAE))
    wings = _both(union(_ellipse(UPPER_C, UPPER_W, UPPER_H, UPPER_ANGLE), _ellipse(LOWER_C, LOWER_W, LOWER_H, LOWER_ANGLE)))
    butterfly = union(body, head, antennae, wings)
    butterfly = butterfly.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    spots = _both(union(*(dot(*s) for s in SPOTS)))
    return butterfly.difference(spots)


motif = Motif(name="butterfly", issue=89, draw=draw)
