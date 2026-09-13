"""A poo emoji, silhouette only: three stacked coils, each narrower than the
one below and set a little off to alternate sides so the pile reads as a
swirl, sitting on a flat base, with a tapered tip rising from the top coil
and hooking over to the right. Where each coil sits on the one below, a
standing crease follows the underside of the upper coil, stopping short of
the outline so the silhouette stays whole. No face."""

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import union
from ..motif import Motif

COILS = [((0.0, -5.4), 22.0, 11.0), ((-0.7, -0.6), 16.0, 7.6), ((0.5, 3.2), 11.0, 5.8)]  # (centre, width, height) ellipses, bottom to top
BASE = -9.6  # the bottom coil is cut flat here
BASE_R = 2.8  # rounds the two corners of the flat base
TIP = [(0.5, 3.2), (-0.8, 8.4), (4.2, 12.0), (6.6, 7.8)]  # cubic Bezier control points for the curl, from the top coil's centre to the point
TIP_W = (5.8, 1.1)  # width at the start and at the point
CREASE_W = 1.5  # standing, the island minimum
CREASE_GAP = 1.2  # cut left between a crease and the outline, past the channel minimum
ROUND = 0.5  # blunts the point of the tip without shaving its round end
CLOSE = 1.8  # blends the coils into one outline, leaving a soft dip at each overlap
BLEND = 0.6  # blends the tip into the pile without filling the hook


def _ellipse(centre, width, height):
    return affinity.scale(Point(*centre).buffer(1.0, 64), width / 2, height / 2, origin=centre)


def _bezier(p0, p1, p2, p3, n):
    def at(t):
        s = 1 - t
        return tuple(s**3 * a + 3 * s**2 * t * b + 3 * s * t**2 * c + t**3 * d for a, b, c, d in zip(p0, p1, p2, p3))

    return [at(i / n) for i in range(n + 1)]


def _taper(points, w0, w1):
    """A stroke along `points` whose width slides from w0 at the start to w1 at the end."""
    n = len(points) - 1
    return union(*(Point(p).buffer((w0 + (w1 - w0) * i / n) / 2, 16) for i, p in enumerate(points)))


def _crease(coil, centre, inside):
    """The lower arc of `coil`, trimmed to `inside`, as a standing line."""
    lower = coil.exterior.intersection(box(-100, -100, 100, centre[1]))
    return lower.intersection(inside).buffer(CREASE_W / 2, 16)


def draw():
    coils = [_ellipse(*c) for c in COILS]
    coils[0] = coils[0].intersection(box(-100, BASE, 100, 100)).buffer(-BASE_R, 16).buffer(BASE_R, 16)
    pile = union(*coils).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    tip = _taper(_bezier(*TIP, 48), *TIP_W).buffer(-ROUND, 16).buffer(ROUND, 16)
    poo = union(pile, tip).buffer(BLEND, 16).buffer(-BLEND, 16)
    inside = poo.buffer(-(CREASE_GAP + CREASE_W / 2), 16)
    creases = union(*(_crease(coil, c[0], inside) for coil, c in zip(coils[1:], COILS[1:])))
    return poo.difference(creases)


motif = Motif(name="poo", issue=48, draw=draw)
