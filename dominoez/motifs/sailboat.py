"""A sailboat heeling to the right: a fat hull with a rounded bottom
sitting in a wavy water line that merges with its keel, and above it two
bellied sails, a tall mainsail behind and a smaller jib in front, parted
from each other and from the hull by standing gaps so the mast reads as a
bright line between them."""

import math

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import stroke, union
from ..motif import Motif

HULL = [(-10.5, 0.0), (10.5, 0.0), (8.0, -4.8), (-7.5, -4.8)]  # deck line and keel line, before rounding
HULL_ROUND = 1.8  # rounds the hull corners
MAST_U = 0.5  # the mast stands here, as the standing gap between the sails
MAST_TOP = 16.5
SAIL_FOOT = 1.5  # v where both sails' lower corners sit, above the deck
MAIN_CLEW = (-9.0, 1.5)  # boom end of the mainsail
MAIN_BELLY = 2.4  # how far the mainsail's leech bows out
JIB_HEAD = 14.0  # where the jib meets the mast
JIB_TACK = (9.5, 1.5)  # the jib's forward corner at the bow
JIB_BELLY = 1.8
GAP = 1.4  # standing gap between sails and around the mast, past the wall minimum
HEEL = -12.0  # degrees; the boat leans to the right
WATER_SPAN = (-11.5, 12.5)
WAVE_LEN, WAVE_AMP = 8.0, 0.7
WAVE_V = -4.8  # runs through the bottom of the hull
WAVE_W = 2.0
ROUND = 0.55  # blunts the sail corners
CLOSE = 0.8  # blends the hull into the water


def _bowed(a, b, belly, n=24):
    """Points along a curve from a to b that bows out by `belly` to the left of travel."""
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    length = math.hypot(dx, dy)
    nx, ny = -dy / length, dx / length
    return [(ax + dx * t + nx * belly * math.sin(math.pi * t), ay + dy * t + ny * belly * math.sin(math.pi * t)) for t in (i / n for i in range(n + 1))]


def _water():
    u0, u1 = WATER_SPAN
    n = 64
    pts = [(u, WAVE_V + WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN)) for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))]
    return stroke(pts, WAVE_W)


def draw():
    hull = Polygon(HULL).buffer(-HULL_ROUND, 16).buffer(HULL_ROUND, 16)
    head = (MAST_U, MAST_TOP)
    main = Polygon([(MAST_U, SAIL_FOOT)] + _bowed(head, MAIN_CLEW, -MAIN_BELLY))
    jib = Polygon([(MAST_U, SAIL_FOOT)] + _bowed((MAST_U, JIB_HEAD), JIB_TACK, JIB_BELLY))
    mast = stroke([(MAST_U, 0.0), (MAST_U, MAST_TOP + 1.0)], GAP)
    sails = union(main, jib).difference(mast).difference(hull.buffer(GAP, 16))
    sails = sails.buffer(-ROUND, 16).buffer(ROUND, 16)
    boat = affinity.rotate(union(hull, sails), HEEL, origin=(0.0, -2.0))
    hull_in_water = union(affinity.rotate(hull, HEEL, origin=(0.0, -2.0)), _water()).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(boat, hull_in_water)


motif = Motif(name="sailboat", issue=96, draw=draw)
