"""Saturn: one big disc with a fat tilted ring around it. The ring is an
ellipse, thick at its band, and passes behind the planet: where it would
cross the disc it is missing, and a standing gap parts the ring ends from
the planet's edge."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, union
from ..motif import Motif

DISC = (0.0, 0.0, 15.0)  # (u, v, diameter)
RING_A, RING_B = 12.8, 5.0  # semi-axes of the ring's centreline ellipse
RING_W = 2.8  # band thickness
RING_TILT = -18.0  # degrees; the ring rises to the right
GAP = 1.2  # standing gap between the disc and the ring
ROUND = 0.55  # blunts the slivers where the ring's inner edge meets the gap
CLOSE = 0.6  # smooths the ring ends


def draw():
    cu, cv, d = DISC
    disc = Point(cu, cv).buffer(d / 2, 128)
    outer = affinity.scale(Point(cu, cv).buffer(1.0, 256), RING_A + RING_W / 2, RING_B + RING_W / 2, origin=(cu, cv))
    inner = affinity.scale(Point(cu, cv).buffer(1.0, 256), RING_A - RING_W / 2, RING_B - RING_W / 2, origin=(cu, cv))
    ring = affinity.rotate(outer.difference(inner), RING_TILT, origin=(cu, cv))
    ring = ring.difference(disc.buffer(GAP, 128))
    ring = ring.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(disc, ring)


motif = Motif(name="saturn", issue=108, draw=draw)
