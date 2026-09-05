"""A plain heart. The classic construction: a square on its corner with a
circle sitting on each upper edge."""

import math

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

WIDTH = 26.0  # mm across the lobes; the box is 28 wide


def draw():
    d = WIDTH / (1 + math.sqrt(2))  # half-diagonal of the square
    r = d / math.sqrt(2)  # circle radius = half the square's side
    square = affinity.rotate(box(-r, -r, r, r), 45)
    lobes = [Point(-d / 2, d / 2).buffer(r), Point(d / 2, d / 2).buffer(r)]
    heart = union(square, *lobes)
    # Centre it on the face vertically.
    minx, miny, maxx, maxy = heart.bounds
    return affinity.translate(heart, yoff=-(miny + maxy) / 2)


motif = Motif(name="heart", issue=18, draw=draw)
