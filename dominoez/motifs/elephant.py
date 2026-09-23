"""A cartoon elephant, side on, facing right: a big round body, a round
head with a big standing D-shaped ear, a smooth gently tapered trunk
hanging forward and curling softly at the tip, two stout legs and a short
tail. The eye is a standing dot."""

import math

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (-3.0, 0.0), 14.0, 11.0
HEAD_C, HEAD_R = (5.5, 3.0), 5.0
TRUNK = [(8.5, 1.5), (10.6, 0.2), (11.6, -2.3), (11.8, -5.0)]  # centreline hanging forward and down from the face to the top of the curl
CURL_C, CURL_R = (9.0, -5.0), 2.8  # the tip curls on this circle, clockwise from the end of TRUNK
CURL_SWEEP = 215.0  # degrees of curl
TRUNK_W0, TRUNK_W1 = 3.4, 2.6  # trunk width at the face and at the tip
TRUNK_STEPS = 60  # dots laid along the centreline to make the taper
EAR_C, EAR_W, EAR_H = (4.3, 2.8), 4.4, 5.6  # standing oval on the back of the head, cut flat at the front into a D
EAR_FRONT = 5.9  # u of the ear's flat front edge
EYE = (8.0, 4.0, 1.9)  # standing (u, v, diameter); keeps more than a channel of cut to the ear and the head edge
LEGS = [[(-7.0, -4.0), (-7.0, -9.0)], [(1.0, -4.0), (1.0, -9.0)]]  # stout columns
LEG_W = 3.6
TAIL = [(-9.8, 1.5), (-11.3, -3.0)]
TAIL_W = 1.6
ROUND = 0.5  # blunts tips and rounds the feet; applied last, so it removes any cut narrower than twice this
CLOSE = 1.0  # fills the creases where the head, trunk and legs meet the body


def _ellipse(c, w, h):
    return affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def _trunk():
    """One smooth stroke with a gentle taper: dots of shrinking diameter along the centreline and round the curl."""
    path = list(TRUNK)
    cu, cv = CURL_C
    for i in range(1, 25):
        a = math.radians(-CURL_SWEEP * i / 24)
        path.append((cu + CURL_R * math.cos(a), cv + CURL_R * math.sin(a)))
    lengths = [0.0]
    for (u0, v0), (u1, v1) in zip(path, path[1:]):
        lengths.append(lengths[-1] + math.hypot(u1 - u0, v1 - v0))
    total = lengths[-1]
    dots = []
    for i in range(TRUNK_STEPS + 1):
        s = total * i / TRUNK_STEPS
        k = max(j for j in range(len(path) - 1) if lengths[j] <= s)
        f = (s - lengths[k]) / (lengths[k + 1] - lengths[k])
        u = path[k][0] + f * (path[k + 1][0] - path[k][0])
        v = path[k][1] + f * (path[k + 1][1] - path[k][1])
        dots.append(dot(u, v, TRUNK_W0 + (TRUNK_W1 - TRUNK_W0) * s / total))
    return union(*dots)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    trunk = _trunk()
    legs = union(*(stroke(l, LEG_W, cap="flat") for l in LEGS))
    tail = stroke(TAIL, TAIL_W)
    elephant = union(body, head, trunk, legs, tail)
    elephant = elephant.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    ear = _ellipse(EAR_C, EAR_W, EAR_H).intersection(box(EAR_C[0] - EAR_W, EAR_C[1] - EAR_H, EAR_FRONT, EAR_C[1] + EAR_H))
    standing = union(ear, dot(*EYE))
    # The opening comes last, so it also removes the sliver of cut left where the head meets the body.
    return elephant.difference(standing).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="elephant", issue=87, draw=draw)
