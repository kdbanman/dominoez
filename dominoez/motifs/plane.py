"""An airliner seen from above, nose up. A long fuselage with an ogive nose
and a rounded tail, two fat swept-back wings, a smaller swept tailplane, and
a standing cockpit window dot at the nose."""

from shapely.geometry import Point, Polygon

from ..geometry import dot, union
from ..motif import Motif

BODY_W = 4.4  # fuselage width
BODY_TOP, BODY_BOTTOM = 8.5, -8.0  # tail end to where the nose cone starts
NOSE_H = 3.5  # nose cone above BODY_TOP
WING = [(1.6, 3.0), (12.0, -4.0), (12.0, -6.5), (1.6, -3.5)]  # right wing, root to tip; the left is mirrored
TAIL = [(1.6, -6.0), (6.5, -9.5), (6.5, -11.0), (1.6, -9.0)]  # right tailplane; the left is mirrored
COCKPIT = (0.0, 7.0, 1.6)  # standing dot at the nose (u, v, diameter)
ROUND = 0.6  # blunts the wing and tailplane tips, past half the channel minimum


def _mirror(points):
    return [(-u, v) for u, v in points]


def _blunt(poly):
    return poly.buffer(-ROUND, 8).buffer(ROUND, 8)


def draw():
    half = BODY_W / 2
    # Fuselage: a rounded-tail tube with an ogive nose.
    tube = Polygon([(-half, BODY_BOTTOM), (half, BODY_BOTTOM), (half, BODY_TOP), (-half, BODY_TOP)])
    tail_cap = Point(0, BODY_BOTTOM).buffer(half, 32)
    r = (half**2 + NOSE_H**2) / (2 * half)
    nose = Point(half - r, BODY_TOP).buffer(r, 128).intersection(Point(-half + r, BODY_TOP).buffer(r, 128))
    nose = nose.intersection(Polygon([(-half, BODY_TOP), (half, BODY_TOP), (half, BODY_TOP + NOSE_H), (-half, BODY_TOP + NOSE_H)]))
    fuselage = union(tube, tail_cap, nose)
    wings = [_blunt(Polygon(WING)), _blunt(Polygon(_mirror(WING)))]
    tails = [_blunt(Polygon(TAIL)), _blunt(Polygon(_mirror(TAIL)))]
    plane = union(fuselage, *wings, *tails)
    return plane.difference(dot(*COCKPIT))


motif = Motif(name="plane", issue=50, draw=draw)
