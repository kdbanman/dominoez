"""A sunflower head, face on: a big central disc ringed by eight fat
petals, each a teardrop with its round end against the disc and its
point outward, parted from the disc by a thin standing ring. The petals
are turned a few degrees off the even spacing so the ring does not look
machined."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import union
from ..motif import Motif

DISC_R = 5.3  # the seed disc
RING = 1.2  # standing ring between the disc and the petals
PETALS = 8
PETAL_BASE_R = 2.7  # radius of each petal's round base; the bases nearly touch, with a wall past the minimum between them
PETAL_TIP = 13.5  # radius of each petal's point, well past its round base so the petal comes to a point
PETAL_C = DISC_R + RING + PETAL_BASE_R  # radius of each petal's base centre
WOBBLE = [1.5, -1.5, 1.0, -2.0, 0.5, -1.5, 1.5, -1.0]  # degrees nudged off the even spacing, one per petal; neighbours differ by 3 at most so the walls hold
ROUND = 0.7  # blunts each petal's point


def _petal(i):
    angle = 90.0 + 360.0 * i / PETALS + WOBBLE[i]
    base = Point(PETAL_C, 0.0).buffer(PETAL_BASE_R, 48)
    drop = union(base, Point(PETAL_TIP, 0.0)).convex_hull
    return affinity.rotate(drop, angle, origin=(0, 0))


def draw():
    petals = union(*(_petal(i) for i in range(PETALS))).buffer(-ROUND, 16).buffer(ROUND, 16)
    disc = Point(0, 0).buffer(DISC_R, 96)
    return union(disc, petals.difference(Point(0, 0).buffer(DISC_R + RING, 96)))


motif = Motif(name="sunflower", issue=124, draw=draw)
