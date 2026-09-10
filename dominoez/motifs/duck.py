"""A rubber duck, side view, facing right. A fat body, a round head, a stubby
beak, and a tail cocked up at the back. The eye is a standing dot."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, union
from ..motif import Motif

# Everything in mm. The box is 28 wide, so the duck is a touch under that.
BODY_W, BODY_H = 22.0, 12.0  # ellipse axes
HEAD_R = 6.0
HEAD_C = (4.0, 9.5)
EYE_D = 2.2
# The beak is a blunt wedge off the front of the head; its corners get rounded.
BEAK = [(7.0, 11.5), (14.0, 10.0), (14.0, 8.0), (7.0, 6.5)]
# The tail rises from the back of the body to a blunt point.
TAIL = [(-5.0, 3.0), (-13.0, 9.0), (-12.5, 4.0), (-9.0, -2.0)]
ROUND = 0.9  # radius of the blunt tips, above half the channel minimum


def _blunt(poly: Polygon) -> Polygon:
    """Round every convex corner: erode then dilate by the same amount."""
    return poly.buffer(-ROUND, 16).buffer(ROUND, 16)


def draw():
    body = affinity.scale(Point(0, 0).buffer(1.0, 64), BODY_W / 2, BODY_H / 2)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    beak = _blunt(Polygon(BEAK))
    tail = _blunt(Polygon(TAIL))
    duck = union(body, head, beak, tail)
    # Fill the crease where the head meets the back, so no sliver of standing
    # material narrows below the wall minimum.
    duck = duck.buffer(1.0, 16).buffer(-1.0, 16)
    eye = dot(HEAD_C[0] + 2.3, HEAD_C[1] + 1.5, EYE_D)
    return duck.difference(eye)


motif = Motif(name="duck", issue=9, draw=draw)
