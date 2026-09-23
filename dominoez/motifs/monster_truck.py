"""A monster truck seen from the side, facing right, caught on a bounce with
its nose in the air: a tiny pickup body with one standing cab window perched
on two giant wheels with standing hubs, the wheels snugged up under the
body with only a thin standing gap between tyre and body."""

from shapely import affinity
from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

WHEEL_R = 6.0  # giant
GAP = 1.2  # standing gap between the top of each tyre and the body's underside
BODY_FLOOR = 1.5  # v of the body's underside
WHEELS = [(-6.8, BODY_FLOOR - GAP - WHEEL_R), (6.8, BODY_FLOOR - GAP - WHEEL_R)]
HUB_D = 3.2  # standing
BED = (-10.0, BODY_FLOOR, -2.5, 5.0)  # (u0, v0, u1, v1) pickup bed
CAB = [(-3.5, BODY_FLOOR), (-3.5, 9.5), (1.5, 9.5), (4.0, 5.5), (4.0, BODY_FLOOR)]
HOOD = (3.0, BODY_FLOOR, 10.5, 5.5)
WINDOW = [(-2.2, 5.5), (-2.2, 8.3), (1.0, 8.3), (2.6, 5.5)]  # standing
TILT = 12.0  # degrees, nose up
ROUND = 0.8  # blunts the window's corners
CORNER = 1.0  # rounds the hood's nose


def _rounded(g, r):
    return g.buffer(-r, 16).buffer(r, 16)


def draw():
    body = union(box(*BED), Polygon(CAB), _rounded(box(*HOOD), CORNER), box(HOOD[0], HOOD[1], HOOD[2] - CORNER, HOOD[3]))
    body = _rounded(body, 0.5)
    body = body.difference(_rounded(Polygon(WINDOW), ROUND))
    wheels = [Point(u, v).buffer(WHEEL_R, 64).difference(dot(u, v, HUB_D)) for u, v in WHEELS]
    truck = union(body, *wheels)
    return affinity.rotate(truck, TILT, origin=(0, 0))


motif = Motif(name="monster_truck", issue=106, draw=draw)
