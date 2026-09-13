"""A lifted 4x4 pickup seen from the side, facing right. Big tires with
standing hubs sit under wheel arches with a wall of air above them, the body
rides high, and the cab has a standing window, a light bar on the roof and a
standing headlight on the hood."""

from shapely.geometry import Point, Polygon, box

from ..geometry import dot, union
from ..motif import Motif

BED = (-13.0, -2.5, -3.4, 3.0)
CAB = [(-2.2, -2.5), (-2.2, 8.5), (2.8, 8.5), (6.0, 3.5), (6.0, -2.5)]
HOOD = (5.0, -2.5, 13.4, 3.5)
LIGHT_BAR = (-1.4, 8.5, 2.2, 9.7)
WINDOW = [(-1.0, 4.0), (-1.0, 7.3), (2.2, 7.3), (4.3, 4.0)]  # standing, a wall inside the cab
HEADLIGHT = (11.5, 1.0, 1.6)  # standing (u, v, diameter)
WHEELS = [(-7.0, -6.5), (7.0, -6.5)]
TIRE_R = 4.8
ARCH_R = 6.0  # the body is cut away this far from each hub, leaving a wall of air over the tire
HUB_D = 3.2  # standing
ROUND = 0.8  # blunts the window's corners, past half the island minimum
CORNER = 1.0  # rounds the hood's nose and the light bar


def _rounded(poly, r):
    return poly.buffer(-r, 8).buffer(r, 8)


def draw():
    body = union(
        box(*BED),
        Polygon(CAB),
        _rounded(box(*HOOD), CORNER),
        box(HOOD[0], HOOD[1], HOOD[2] - CORNER, HOOD[3]),  # only the nose is rounded
        _rounded(box(*LIGHT_BAR), 0.5),
    )
    for u, v in WHEELS:
        body = body.difference(Point(u, v).buffer(ARCH_R, 32))
    body = body.difference(_rounded(Polygon(WINDOW), ROUND))
    body = body.difference(dot(*HEADLIGHT))
    tires = [Point(u, v).buffer(TIRE_R, 48).difference(dot(u, v, HUB_D)) for u, v in WHEELS]
    return union(body, *tires)


motif = Motif(name="truck", issue=13, draw=draw)
