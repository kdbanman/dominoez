"""The signage sun: a big disc with eight fat triangular rays around it,
one straight up, parted from the disc by a standing ring."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import union
from ..motif import Motif

DISC_R = 6.0
RING = 1.5  # standing gap between the disc and the rays
RAYS = 8
RAY_BASE_R = DISC_R + RING  # the rays start at the outer edge of the ring
RAY_LEN = 6.4  # each ray is a triangle this long before its tip is blunted
RAY_TIP_R = RAY_BASE_R + RAY_LEN  # the sun spans about 25 mm once the tips are blunted
RAY_HALF_BASE = 2.45  # half the width of a ray at its base; the wall left between neighbouring bases is past the minimum once the corners are rounded
ROUND = 0.7  # blunts each ray's tip and base corners


def _ray(i):
    angle = 90.0 + 360.0 * i / RAYS
    tri = Polygon([(RAY_BASE_R - 0.5, -RAY_HALF_BASE), (RAY_TIP_R, 0.0), (RAY_BASE_R - 0.5, RAY_HALF_BASE)])
    return affinity.rotate(tri, angle, origin=(0, 0))


def draw():
    rays = union(*(_ray(i) for i in range(RAYS))).buffer(-ROUND, 16).buffer(ROUND, 16)
    rays = rays.difference(Point(0, 0).buffer(RAY_BASE_R, 96))
    return union(Point(0, 0).buffer(DISC_R, 96), rays)


motif = Motif(name="sun", issue=127, draw=draw)
