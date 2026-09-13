"""A cute toadstool, as in the mushroom emoji: a plump domed cap, wider than
it is tall, overhanging a short chubby stalk that curves out at its foot.
Four standing spots of different sizes sit unevenly on the cap, and a thin
standing gill line parts the cap's rim from the stalk."""

from shapely import affinity
from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

CAP_W, CAP_H = 25.0, 26.0  # ellipse axes; the cap is the part above the rim
CAP_C = (0.0, 1.0)  # the rim sits a little below the centre so the sides bulge
RIM = 0.0  # v of the cap's underside
CAP_ROUND = 2.0  # rounds the rim's corners
SPOTS = [(-4.6, 8.2, 4.2), (4.4, 9.8, 3.2), (8.4, 4.4, 2.6), (-9.0, 4.0, 2.2)]  # standing (u, v, diameter)
GILL = 1.2  # standing gap between rim and stalk
STALK_TOP, STALK_BOTTOM = RIM - GILL, -10.0
STALK_HALF_TOP, STALK_HALF_BOTTOM = 5.2, 8.0  # half-widths at the top and the foot
STALK_FLARE = 1.8  # exponent of the side curve: higher keeps the sides straight longer before they curve out
STALK_ROUND = 1.6  # rounds the foot's corners
STALK_TOP_ROUND = 0.4  # softens the corners under the gill line
STEPS = 24


def stalk_side(t: float) -> float:
    """Half-width of the stalk at fraction t of the way from top to foot."""
    return STALK_HALF_TOP + (STALK_HALF_BOTTOM - STALK_HALF_TOP) * t**STALK_FLARE


def draw():
    cap = affinity.scale(Point(*CAP_C).buffer(1.0, 64), CAP_W / 2, CAP_H / 2, origin=CAP_C)
    cap = cap.intersection(box(-CAP_W, RIM, CAP_W, CAP_C[1] + CAP_H))
    cap = cap.buffer(-CAP_ROUND, 16).buffer(CAP_ROUND, 16)

    # the sides are drawn up to the rim so the foot rounding leaves the top square, then clipped under the gill line
    vs = [RIM + (STALK_BOTTOM - RIM) * i / STEPS for i in range(STEPS + 1)]
    right = [(stalk_side(i / STEPS), v) for i, v in enumerate(vs)]
    left = [(-u, v) for u, v in reversed(right)]
    stalk = Polygon(right + left).buffer(-STALK_ROUND, 16).buffer(STALK_ROUND, 16)
    stalk = stalk.intersection(box(-CAP_W, STALK_BOTTOM - 1, CAP_W, STALK_TOP))
    stalk = stalk.buffer(-STALK_TOP_ROUND, 8).buffer(STALK_TOP_ROUND, 8)

    return union(cap.difference(union(*(dot(*s) for s in SPOTS))), stalk)


motif = Motif(name="mushroom", issue=38, draw=draw)
