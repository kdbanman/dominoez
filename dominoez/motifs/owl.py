"""A cartoon owl, front-on: a plump egg body with two ear tufts, a standing
face mask of two big eye discs joined by a beak, each disc with a cut
pupil, and two small feet at the bottom."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, union
from ..motif import Motif

BODY_C, BODY_W, BODY_H = (0.0, -1.5), 20.0, 20.0  # round body
TUFTS = [[(-8.8, 11.5), (-3.0, 8.5), (-9.0, 6.0)], [(8.8, 11.5), (3.0, 8.5), (9.0, 6.0)]]  # ear tufts
EYES = [(-3.4, 3.5), (3.4, 3.5)]  # centres of the standing eye discs
EYE_R = 3.5  # the discs just overlap into one mask
PUPIL_D = 2.4  # cut dot in each disc
BEAK = [(-2.6, 2.4), (2.6, 2.4), (0.0, -1.8)]  # standing wedge joining the discs
FEET = [(-3.4, -12.4), (3.4, -12.4)]
FOOT_W, FOOT_H = 4.6, 2.3
ROUND = 0.6  # blunts the tuft tips
CLOSE = 1.0  # fills the creases where the tufts and feet meet the body
MASK_CLOSE = 0.8  # fills the cusps where the eye discs meet each other and the beak
MASK_ROUND = 0.5  # blunts the beak tip


def _ellipse(c, w, h):
    return affinity.scale(Point(*c).buffer(1.0, 64), w / 2, h / 2, origin=c)


def draw():
    body = _ellipse(BODY_C, BODY_W, BODY_H)
    tufts = union(*(Polygon(t) for t in TUFTS))
    feet = union(*(_ellipse(c, FOOT_W, FOOT_H) for c in FEET))
    owl = union(body, tufts, feet)
    owl = owl.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    mask = union(*(Point(*c).buffer(EYE_R, 64) for c in EYES), Polygon(BEAK))
    mask = mask.buffer(MASK_CLOSE, 16).buffer(-MASK_CLOSE, 16).buffer(-MASK_ROUND, 16).buffer(MASK_ROUND, 16)
    pupils = union(*(dot(u, v, PUPIL_D) for u, v in EYES))
    return union(owl.difference(mask), pupils)


motif = Motif(name="owl", issue=85, draw=draw)
