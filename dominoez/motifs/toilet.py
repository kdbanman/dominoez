"""A toilet seen from the side, bowl to the right. Tank with its lid, seat
overhanging the bowl, a pedestal flaring at the floor, all one silhouette.
Standing lines part the lid from the tank and the seat from the bowl."""

from shapely.geometry import Point, Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

LINE_W = 1.2  # standing lines, above the wall minimum


def _rounded(poly, r):
    return poly.buffer(-r, 8).buffer(r, 8)


def draw():
    tank = _rounded(box(-9.0, -1.0, -3.0, 11.0), 1.0)
    lid = _rounded(box(-9.6, 10.4, -2.4, 12.2), 0.6)
    handle = _rounded(box(-3.2, 7.6, -1.2, 9.2), 0.4)
    seat = _rounded(box(-4.0, -0.2, 10.5, 1.6), 0.6)
    bowl = union(box(-4.0, -6.0, 4.0, -0.2), Point(4.0, -1.0).buffer(5.0, 32).intersection(box(-1.0, -6.0, 9.2, -0.2)))
    pedestal = _rounded(Polygon([(-4.5, -12.0), (4.5, -12.0), (3.5, -11.0), (3.0, -6.0), (-3.0, -6.0), (-3.5, -11.0)]), 0.5)
    body = union(tank, lid, handle, seat, bowl, pedestal)
    lid_line = stroke([(-10.2, 10.0), (-2.0, 10.0)], LINE_W, cap="flat")
    seat_line = stroke([(-1.0, -0.9), (10.2, -0.9)], LINE_W, cap="flat")
    return body.difference(lid_line).difference(seat_line)


motif = Motif(name="toilet", issue=8, draw=draw)
