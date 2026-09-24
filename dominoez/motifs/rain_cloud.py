"""A rain cloud: a puffy cloud, three round lobes over a flat base, with
three fat teardrops falling from it, the middle one lower than the outer
two."""

from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

LOBES = [((-6.8, 1.0), 5.2), ((0.5, 3.6), 6.6), ((7.2, 0.6), 4.8)]  # (centre, radius) of each puff
BASE = (-11.0, -3.5, 11.2, 1.5)  # the flat underside, a box the lobes sit on
BASE_ROUND = 1.6  # rounds the base's corners
CLOSE = 1.5  # fills the creases between the puffs
DROPS = [(-6.5, -11.6), (0.5, -14.2), (7.0, -11.6)]  # centre of each drop's round bottom; the tips hang clear of the cloud
DROP_R = 2.3  # radius of the round bottom
DROP_TIP = 6.4  # height of the tip above the round bottom's centre
ROUND = 0.6  # blunts each drop's tip


def _drop(u, v):
    bottom = Point(u, v).buffer(DROP_R, 48)
    return union(bottom, Point(u, v + DROP_TIP)).convex_hull


def draw():
    cloud = union(*(Point(*c).buffer(r, 64) for c, r in LOBES), box(*BASE).buffer(-BASE_ROUND, 16).buffer(BASE_ROUND, 16))
    cloud = cloud.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    drops = union(*(_drop(*d) for d in DROPS)).buffer(-ROUND, 16).buffer(ROUND, 16)
    return union(cloud, drops)


motif = Motif(name="rain_cloud", issue=128, draw=draw)
