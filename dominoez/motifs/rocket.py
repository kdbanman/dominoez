"""A cartoon rocket, nose up. A capsule body with a pointed nose, two fins,
a round porthole left standing, and a flame below."""

from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

BODY_W = 13.0
BODY_H = 30.0  # of the straight-sided part, before the nose
NOSE_H = 11.0
FIN_W = 5.5  # how far each fin sticks out past the body
FIN_H = 12.0  # from the fin's lowest point up to where it leaves the body
FIN_DROP = 2.0  # how far the fins hang below the body
WINDOW_D = 5.5
FLAME_W, FLAME_H = 7.0, 9.0
GAP = 1.6  # standing material between the body and the flame, above the wall minimum
ROUND = 0.9  # radius of every blunt tip, above half the channel minimum


def _blunt(poly: Polygon) -> Polygon:
    """Round every convex corner: erode then dilate by the same amount."""
    return poly.buffer(-ROUND, 16).buffer(ROUND, 16)


def draw():
    half = BODY_W / 2
    bottom = -BODY_H / 2
    top = -bottom
    # Body: a rectangle with rounded bottom corners.
    body = box(-half, bottom, half, top).buffer(-2, 16).buffer(2, 16).union(box(-half, bottom + 2, half, top))
    # Nose: an ogive, the intersection of two big circles, sitting on the body.
    r = (half**2 + NOSE_H**2) / (2 * half)
    nose = Point(half - r, top).buffer(r, 128).intersection(Point(-half + r, top).buffer(r, 128))
    nose = nose.intersection(box(-half, top, half, top + NOSE_H))
    # Fins: swept-back, overlapping into the body so their rounded corners are hidden.
    fin_bottom = bottom - FIN_DROP
    fin_r = Polygon([(half - 2, fin_bottom + FIN_H), (half + FIN_W, fin_bottom), (half - 2, fin_bottom)])
    fin_l = Polygon([(-u, v) for u, v in fin_r.exterior.coords])
    rocket = union(body, nose, _blunt(fin_l), _blunt(fin_r))
    # Porthole: a standing disc in the upper body.
    rocket = rocket.difference(dot(0, top - 6.5, WINDOW_D))
    # Flame: a blunt teardrop hanging under the body, parted from it by a wall.
    fy = fin_bottom - GAP
    flame = _blunt(Polygon([(-FLAME_W / 2, fy), (FLAME_W / 2, fy), (0, fy - FLAME_H)]))
    return union(rocket, flame)


motif = Motif(name="rocket", issue=7, draw=draw)
