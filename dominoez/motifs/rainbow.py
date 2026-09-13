"""A rainbow: three nested half-ring bands over a flat base, each band a
cut channel parted from the next by a thin standing line."""

from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

OUTER_R = 13.0  # outer radius of the top band
BAND_W = 2.4  # each cut band
LINE_W = 1.2  # standing line between bands, above the wall minimum
BANDS = 3


def _band(outer: float):
    ring = Point(0, 0).buffer(outer, 128).difference(Point(0, 0).buffer(outer - BAND_W, 128))
    return ring.intersection(box(-outer, 0, outer, outer))


def draw():
    return union(*(_band(OUTER_R - i * (BAND_W + LINE_W)) for i in range(BANDS)))


motif = Motif(name="rainbow", issue=34, draw=draw)
