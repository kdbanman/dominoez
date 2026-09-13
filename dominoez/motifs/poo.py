"""A poo emoji: three stacked coils, each narrower than the one below, with a
pointed tip curling off the top. Two big eyes sit where the bottom coil
meets the middle one and a wide smile sits below them, all left standing,
with a standing crease under the top coil so the stack reads as a swirl."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

COILS = [((0.0, -7.5), 23.0, 11.0), ((0.5, -1.5), 16.5, 9.0), ((1.0, 3.5), 10.5, 7.0)]  # (centre, width, height) ellipses, bottom to top
TIP = [(-2.0, 4.5), (4.5, 5.0), (4.0, 11.0)]  # a pointed wedge curling up from the top coil
CREASE = [(-3.5, 0.3), (1.0, -0.7), (5.0, 0.3)]  # standing, under the top coil
CREASE_W = 1.6  # past the island minimum
EYES = [(-3.6, -4.0), (3.6, -4.0)]  # standing
EYE_D = 3.2
SMILE = [(-5.0, -8.6), (-2.5, -10.2), (0.0, -10.7), (2.5, -10.2), (5.0, -8.6)]  # standing
SMILE_W = 1.6
ROUND = 0.7  # blunts the tip past half the channel minimum
CLOSE = 1.2  # fills the creases where the coils overlap


def _ellipse(centre, width, height):
    return affinity.scale(Point(*centre).buffer(1.0, 64), width / 2, height / 2, origin=centre)


def draw():
    coils = [_ellipse(*c) for c in COILS]
    tip = Polygon(TIP).buffer(-ROUND, 8).buffer(ROUND, 8)
    poo = union(*coils, tip).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    features = union(stroke(CREASE, CREASE_W), *(dot(u, v, EYE_D) for u, v in EYES), stroke(SMILE, SMILE_W))
    return poo.difference(features)


motif = Motif(name="poo", issue=48, draw=draw)
