"""A comet: a round head at the upper right with a fat tail sweeping away
down and to the left, as wide as the head where it leaves it and tapering
to a blunt tip, with a thinner streak on either side of the tail, each
parted from it by a standing gap."""

from shapely.geometry import LineString, Point

from ..geometry import dot, union
from ..motif import Motif

HEAD = (7.0, 6.5, 10.0)  # (u, v, diameter)
TAIL = [(5.5, 5.0), (-1.0, 1.0), (-7.0, -4.0), (-11.0, -9.5)]  # centreline from inside the head, sweeping down-left
TAIL_W0, TAIL_W1 = 9.0, 1.8
STREAKS = [
    [(1.0, 11.0), (-5.0, 7.5), (-9.0, 3.5)],  # above the tail, running back from beside the head
    [(6.0, -0.5), (0.5, -4.0), (-3.0, -8.0)],  # below the tail
]
STREAK_W0, STREAK_W1 = 3.4, 1.4
GAP = 1.4  # standing gap between the tail and each streak
ROUND = 0.6  # blunts the tail tips
CLOSE = 0.8  # blends the tail root into the head


def _taper(points, w0, w1, n=32):
    """A path buffered with a width that eases from w0 at the start to w1 at the end."""
    ls = LineString(points)
    discs = []
    for i in range(n + 1):
        t = i / n
        p = ls.interpolate(t, normalized=True)
        discs.append(Point(p.x, p.y).buffer((w0 + (w1 - w0) * t) / 2, 24))
    return union(*(union(discs[i], discs[i + 1]).convex_hull for i in range(n)))


def draw():
    body = union(dot(*HEAD), _taper(TAIL, TAIL_W0, TAIL_W1))
    body = body.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    streaks = union(*(_taper(s, STREAK_W0, STREAK_W1) for s in STREAKS)).difference(body.buffer(GAP, 16))
    comet = union(body, streaks)
    return comet.buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="comet", issue=111, draw=draw)
