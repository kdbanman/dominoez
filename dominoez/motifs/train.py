"""A steam locomotive seen from the side, facing right. Cab with a standing
window, boiler with a dome and a flared stack, three drive wheels and a
leading wheel with standing hubs, a cowcatcher, and two puffs of smoke."""

from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

CAB = (-12.0, -2.5, -6.5, 7.5)
ROOF = (-12.6, 7.0, -5.9, 8.4)
WINDOW = (-11.0, 2.5, -7.8, 6.0)  # standing
BOILER = (-6.5, -2.5, 7.5, 3.5)
NOSE_C, NOSE_R = (7.5, 0.5), 3.0  # rounds the boiler's front
STACK = [(5.0, 3.0), (8.4, 3.0), (9.0, 7.6), (4.4, 7.6)]
DOME_C, DOME_R = (-1.5, 3.3), 2.0
CHASSIS = (-12.0, -4.0, 11.5, -2.0)
WHEELS = [(-9.8, -5.4, 2.6), (-3.2, -5.4, 2.6), (3.4, -5.4, 2.6), (9.2, -5.4, 2.0)]  # (u, v, radius)
HUB_D = 1.6  # standing
COWCATCHER = [(11.4, -2.0), (13.2, -2.0), (13.2, -6.2)]
SMOKE = [(8.0, 10.0, 2.4), (10.6, 12.2, 1.8)]
ROUND = 0.6
CLOSE = 0.55  # fills the crease where the boiler's nose meets the chassis, below half any gap


def _rounded(poly):
    return poly.buffer(-ROUND, 8).buffer(ROUND, 8)


def draw():
    loco = union(
        box(*CAB),
        _rounded(box(*ROOF)),
        box(*BOILER),
        Point(*NOSE_C).buffer(NOSE_R, 32),
        _rounded(Polygon(STACK)),
        Point(*DOME_C).buffer(DOME_R, 32),
        box(*CHASSIS),
        *(Point(u, v).buffer(r, 32) for u, v, r in WHEELS),
        _rounded(Polygon(COWCATCHER)),
    )
    loco = loco.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    loco = loco.difference(box(*WINDOW))
    for u, v, _ in WHEELS:
        loco = loco.difference(dot(u, v, HUB_D))
    return union(loco, *(dot(u, v, d) for u, v, d in SMOKE))


motif = Motif(name="train", issue=12, draw=draw)
