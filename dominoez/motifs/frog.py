"""A cartoon frog sitting front-on: a wide squat body with two bulging eyes
sitting on top, fat haunches at either side, big back feet splayed out and
two small front feet tucked under the chin. The pupils and a wide smile are
standing."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (0.0, -1.0), 20.0, 13.0  # squat body
EYES = [(-5.0, 5.2), (5.0, 5.2)]  # centres of the eye bulges, sunk into the top of the body
EYE_R = 3.8
PUPIL_D = 2.2  # standing dot in each eye
HAUNCHES = [(-9.0, -4.0), (9.0, -4.0)]
HAUNCH_R = 4.2
BACK_FEET = [(-11.0, -8.2), (11.0, -8.2)]  # splayed out beside the haunches
BACK_FOOT_W, BACK_FOOT_H = 5.5, 2.6
FRONT_FEET = [(-3.8, -8.0), (3.8, -8.0)]  # tucked under the chin
FRONT_FOOT_W, FRONT_FOOT_H = 4.6, 2.6
SMILE = [(-6.0, 0.8), (-3.0, -0.8), (0.0, -1.3), (3.0, -0.8), (6.0, 0.8)]  # standing
SMILE_W = 1.6
ROUND = 0.5  # blunts tips
CLOSE = 1.0  # fills the creases where the eyes, feet and haunches meet the body


def _ellipse(c, w, h):
    return affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    eyes = union(*(Point(*c).buffer(EYE_R, 64) for c in EYES))
    haunches = union(*(Point(*c).buffer(HAUNCH_R, 64) for c in HAUNCHES))
    back_feet = union(*(_ellipse(c, BACK_FOOT_W, BACK_FOOT_H) for c in BACK_FEET))
    front_feet = union(*(_ellipse(c, FRONT_FOOT_W, FRONT_FOOT_H) for c in FRONT_FEET))
    frog = union(body, eyes, haunches, back_feet, front_feet)
    frog = frog.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    standing = union(*(dot(u, v + 0.3, PUPIL_D) for u, v in EYES), stroke(SMILE, SMILE_W))
    return frog.difference(standing)


motif = Motif(name="frog", issue=84, draw=draw)
