"""A cartoon toadstool: a wide domed cap with three standing spots, sitting on
a stalk that flares out at the foot. A standing wall parts cap from stalk so
the cap's rim reads."""

from shapely import affinity
from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

CAP_W, CAP_H = 24.0, 22.0  # ellipse axes
CAP_C = (0.0, 1.0)
CAP_FLOOR = 1.0  # the cap is the ellipse above this line
SPOTS = [(-5.5, 5.0, 3.4), (2.5, 7.0, 3.8), (7.5, 4.0, 2.8)]  # standing (u, v, diameter)
STALK = [(-4.0, -0.2), (4.0, -0.2), (5.8, -10.0), (-5.8, -10.0)]  # top edge, then the flared foot
STALK_ROUND = 1.0  # rounds the stalk's corners


def draw():
    cap = affinity.scale(Point(*CAP_C).buffer(1.0, 64), CAP_W / 2, CAP_H / 2, origin=CAP_C)
    cap = cap.intersection(box(-CAP_W, CAP_FLOOR, CAP_W, CAP_C[1] + CAP_H))
    stalk = Polygon(STALK).buffer(-STALK_ROUND, 8).buffer(STALK_ROUND, 8)
    spots = union(*(dot(*s) for s in SPOTS))
    return union(cap.difference(spots), stalk)


motif = Motif(name="mushroom", issue=38, draw=draw)
