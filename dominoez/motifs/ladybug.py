"""A ladybug, top-down, head up: a round body with a small round head, a
standing line splitting the wing cases down the middle, three standing spots
on each side, three short legs a side, and two antennae. Symmetric about the
centreline."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_R = (0.0, -1.5), 9.5
HEAD_C, HEAD_R = (0.0, 7.6), 3.8
SPLIT = [(0.0, 5.5), (0.0, -12.5)]  # standing line down the back, running out the bottom
SPLIT_W = 1.4
SPOTS = [(4.5, 3.0), (6.0, -3.0), (3.5, -7.5)]  # standing, right side; mirrored
SPOT_D = 3.0
LEGS = [[(7.5, 3.0), (10.8, 5.5)], [(9.0, -1.5), (12.3, -1.5)], [(7.5, -6.0), (10.5, -8.8)]]  # right side; mirrored
LEG_W = 2.0
ANTENNAE = [[(2.0, 10.3), (4.0, 12.8)]]  # right side; mirrored
ANTENNA_W, ANTENNA_TIP = 1.5, 2.2
ROUND = 0.5  # blunts tips
CLOSE = 0.9  # fills the creases where the head and legs meet the body


def _both(g):
    return union(g, affinity.scale(g, -1.0, 1.0, origin=(0, 0)))


def draw():
    body = Point(*BODY_C).buffer(BODY_R, 64)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    legs = _both(union(*(stroke(l, LEG_W) for l in LEGS)))
    antennae = _both(union(*(union(stroke(a, ANTENNA_W), dot(*a[-1], ANTENNA_TIP)) for a in ANTENNAE)))
    ladybug = union(body, head, legs, antennae)
    ladybug = ladybug.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    standing = union(stroke(SPLIT, SPLIT_W), _both(union(*(dot(u, v, SPOT_D) for u, v in SPOTS))))
    return ladybug.difference(standing)


motif = Motif(name="ladybug", issue=90, draw=draw)
