"""A taco seen end-on: the shell is a thick U, a semicircular band carried
straight up a little at each end, and inside it three horizontal layers
of filling stacked as fat bars parted by thin standing lines, the top
layer a row of bumps peeking above the shell's ends. A thin standing gap
keeps the band a band."""

from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

OUTER_R = 12.0  # outer radius of the shell
BAND = 3.5  # thickness of the shell band
RIM = 0.0  # v where the band's semicircle ends and its straight ends begin
ENDS = 2.5  # the band's ends carry on straight up this far past RIM
GAP = 1.2  # standing line between the band and the filling, and between layers
LAYERS = [(-9.0, -4.2), (-3.0, 0.8)]  # (bottom, top) v of the two flat bars, inside the shell
BUMPS = [(-5.2, 2.6, 2.4), (-1.8, 3.0, 2.6), (1.8, 3.0, 2.6), (5.2, 2.6, 2.4)]  # top layer scallops (u, v, radius)
BUMP_BASE = 2.0  # v where the bumpy layer starts, a line above the top bar
CLOSE = 0.8  # knits the bumps into one layer
ROUND = 0.5  # blunts corners


def draw():
    outer = Point(0, RIM).buffer(OUTER_R, 96)
    inner = Point(0, RIM).buffer(OUTER_R - BAND, 96)
    below = box(-OUTER_R - 1, RIM - OUTER_R - 1, OUTER_R + 1, RIM)
    shell = outer.difference(inner).intersection(below)
    for side in (-1, 1):
        u0, u1 = sorted((side * (OUTER_R - BAND), side * OUTER_R))
        shell = union(shell, box(u0, RIM - 1, u1, RIM + ENDS))
    filling_area = union(Point(0, RIM).buffer(OUTER_R - BAND - GAP, 96), box(-(OUTER_R - BAND - GAP), RIM, OUTER_R - BAND - GAP, RIM + ENDS + 1))
    bars = [filling_area.intersection(box(-OUTER_R, b, OUTER_R, t)) for b, t in LAYERS]
    bumps = union(*(Point(u, v).buffer(r, 32) for u, v, r in BUMPS)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    bumps = bumps.difference(box(-OUTER_R, -OUTER_R, OUTER_R, BUMP_BASE))
    taco = union(shell, *bars, bumps)
    return taco.buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="taco", issue=116, draw=draw)
