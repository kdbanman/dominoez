"""A yin yang: a disc split by an S curve into two teardrops, the right
one cut with a standing dot in its head, the left one standing with a
cut dot in its head, and a fat ring around the whole so the standing
teardrop has an edge. The ring also pulls the centre of mass to the
middle, so the disc is placed square on the face."""

from shapely.geometry import Point, box

from ..geometry import dot, union
from ..motif import Motif

OUTER_D = 25.0  # mm outer diameter of the ring
RING_W = 2.5  # mm width of the ring; heavy enough to balance the cut teardrop
DOT_D = 3.6  # mm diameter of each small dot
OPEN = 0.8  # trims the cut teardrop's tail where it thins to nothing
CLOSE = 0.85  # trims the standing teardrop's tail the same way


def draw():
    outer_r = OUTER_D / 2
    inner_r = outer_r - RING_W
    half_r = inner_r / 2
    disc = Point(0, 0).buffer(inner_r, 96)
    ring = Point(0, 0).buffer(outer_r, 96).difference(disc)
    right_half = disc.intersection(box(0, -outer_r, outer_r, outer_r))
    lower = Point(0, -half_r).buffer(half_r, 64)
    upper = Point(0, half_r).buffer(half_r, 64)
    teardrop = union(right_half, lower).difference(upper)
    cut = union(ring, teardrop).buffer(-OPEN, 16).buffer(OPEN, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    cut = cut.difference(dot(0, -half_r, DOT_D))  # standing dot in the cut teardrop
    return union(cut, dot(0, half_r, DOT_D))  # cut dot in the standing teardrop


motif = Motif(name="yin_yang", issue=161, draw=draw)
