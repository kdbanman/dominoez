"""A pterodactyl in flight seen from below: two broad wings spread as one
wide M, each with a clear finger tip at the wrist, a small body at the
centre with a short tail, and a head held in profile on a short neck,
with a long fat beak forward to the right and a long fat crest sweeping
back to the left, the head about half the span. The eye is a standing dot. Laid out big, then scaled to fit."""

from shapely import affinity
from shapely.geometry import LineString, Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

WING = [(1.5, 2.5), (11.0, 5.0), (14.0, 7.0), (12.5, 2.5), (8.5, -1.5), (2.0, -5.0)]  # right wing: shoulder, wrist, finger tip, then the scalloped trailing edge back to the hip; mirrored for the left
BODY = [(0.0, 4.5), (0.0, -5.0)]  # neck to hip
BODY_W = 4.4
TAIL = [(0.0, -4.0), (0.0, -9.0)]
TAIL_W0, TAIL_W1 = 3.0, 1.5
HEAD = (1.0, 7.8, 5.8)  # (u, v, diameter)
BEAK = [(2.2, 7.8), (9.0, 8.8)]  # skull to beak tip, lifted clear of the wing
BEAK_W0, BEAK_W1 = 4.4, 1.7
CREST = [(0.0, 8.8), (-7.0, 11.8)]  # skull back to crest tip
CREST_W0, CREST_W1 = 4.2, 1.7
EYE = (1.6, 8.0, 1.9)  # standing
ROUND = 0.55  # blunts the beak, crest, finger tips and tail
CLOSE = 0.8  # blends the wings and head into the body
SCALE = 0.92


def _taper(points, w0, w1, n=16):
    """A path buffered with a width that eases from w0 at the start to w1 at the end."""
    ls = LineString(points)
    discs = []
    for i in range(n + 1):
        t = i / n
        p = ls.interpolate(t, normalized=True)
        discs.append(Point(p.x, p.y).buffer((w0 + (w1 - w0) * t) / 2, 24))
    return union(*(union(discs[i], discs[i + 1]).convex_hull for i in range(n)))


def draw():
    wings = union(Polygon(WING), Polygon([(-u, v) for u, v in WING]))
    body = stroke(BODY, BODY_W)
    tail = _taper(TAIL, TAIL_W0, TAIL_W1)
    head = union(dot(*HEAD), _taper(BEAK, BEAK_W0, BEAK_W1), _taper(CREST, CREST_W0, CREST_W1))
    ptero = union(wings, body, tail, head)
    ptero = ptero.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return affinity.scale(ptero.difference(dot(*EYE)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="pterodactyl", issue=93, draw=draw)
