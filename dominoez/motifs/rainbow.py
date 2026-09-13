"""A rainbow: three concentric half-ring bands standing on a flat base,
each parted from the next by a thin standing line. The bands are as thick
as the face allows; a shorter sweep with radial ends reads as a wifi icon,
so the arch keeps the full half circle."""

from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

INNER_R = 2.9  # radius of the hole under the innermost band
BAND = 2.85  # thickness of each cut band
GAP = 1.1  # standing line between bands, past the wall minimum
BANDS = 3
ROUND = 0.4  # blunts the corners where the bands meet the base


def draw():
    parts = []
    r = INNER_R
    for _ in range(BANDS):
        ring = Point(0, 0).buffer(r + BAND, 96).difference(Point(0, 0).buffer(r, 96))
        parts.append(ring)
        r += BAND + GAP
    arch = union(*parts).intersection(box(-r, 0, r, r))
    return arch.buffer(-ROUND, 8).buffer(ROUND, 8)


motif = Motif(name="rainbow", issue=34, draw=draw)
