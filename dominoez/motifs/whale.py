"""An icon whale, side on, head to the left, as one silhouette: a rounded
head, a long back sloping down to a narrow tail stalk that rises to a
two-lobed fluke, and a round belly. The eye is a standing dot."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import dot
from ..motif import Motif

# The outline, counter-clockwise from the nose: over the head and back, up
# the tail stalk, round the fluke, down the stalk and back along the belly.
OUTLINE = [
    (-12.0, -0.5),  # nose
    (-11.6, 1.8), (-10.3, 3.6), (-8.0, 4.8), (-5.0, 5.3), (-1.5, 5.0), (2.0, 4.0), (5.0, 2.8), (7.5, 2.4),  # head and back
    (8.3, 4.0), (8.6, 5.6),  # front of the tail stalk
    (6.0, 7.4), (4.8, 9.4), (6.0, 10.4), (9.6, 8.4), (13.2, 10.4), (14.4, 9.4), (13.2, 7.4),  # fluke, two lobes with a notch
    (11.4, 5.4), (11.2, 3.0), (10.2, 0.5), (8.0, -2.4),  # back of the tail stalk
    (4.0, -4.6), (0.0, -5.6), (-4.5, -5.6), (-8.5, -4.6), (-11.0, -3.0),  # belly
]
EYE = (-9.0, 1.0, 2.0)  # standing (u, v, diameter)
SMOOTH = 3  # rounds of corner cutting on the outline, so it reads as a curve rather than a polygon
ROUND = 1.0  # blunts the nose and fluke tips
CLOSE = 1.2  # rounds the fluke notch
SCALE = 0.93  # the whale is laid out big, then shrunk so the fluke stays inside the box


def _smooth(points, rounds):
    """Chaikin corner cutting on a closed ring: each round replaces every corner with two points a quarter of the way along its edges."""
    for _ in range(rounds):
        cut = []
        for (u0, v0), (u1, v1) in zip(points, points[1:] + points[:1]):
            cut.append((0.75 * u0 + 0.25 * u1, 0.75 * v0 + 0.25 * v1))
            cut.append((0.25 * u0 + 0.75 * u1, 0.25 * v0 + 0.75 * v1))
        points = cut
    return points


def draw():
    whale = Polygon(_smooth(OUTLINE, SMOOTH))
    whale = whale.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(whale.difference(dot(*EYE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="whale", issue=81, draw=draw)
