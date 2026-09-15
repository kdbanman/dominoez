"""A cartoon fish, side on, facing right: a fat oval body with a pointed
dorsal fin on top and a small fin underneath, a forked tail at the left,
and a round eye and a curved gill line left standing near the front."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_W, BODY_H = 16.0, 9.5  # ellipse axes
BODY_C = (1.5, 0.0)
TAIL = [(-5.5, 1.5), (-11.0, 5.2), (-11.8, 3.2), (-9.2, 0.0), (-11.8, -3.2), (-11.0, -5.2), (-5.5, -1.5)]  # forked, root inside the body
DORSAL = [(-2.5, 4.0), (1.0, 8.4), (5.0, 4.0)]
VENTRAL = [(0.0, -4.0), (2.0, -7.0), (5.0, -4.0)]
EYE = (6.0, 1.0, 2.0)  # standing (u, v, diameter)
GILL = [(3.0, 2.4), (2.2, 0.0), (3.0, -2.4)]  # standing
GILL_W = 1.6
ROUND = 0.7  # blunts the cut tips of the fins and tail lobes
CLOSE = 0.8  # fills the creases where the fins and tail meet the body and blunts the tail notch


def draw():
    body = affinity.scale(Point(*BODY_C).buffer(1.0, 64), BODY_W / 2, BODY_H / 2, origin=BODY_C)
    fish = union(body, Polygon(TAIL), Polygon(DORSAL), Polygon(VENTRAL))
    fish = fish.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return fish.difference(union(dot(*EYE), stroke(GILL, GILL_W)))


motif = Motif(name="fish", issue=42, draw=draw)
