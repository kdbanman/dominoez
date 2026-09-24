"""An acorn: a plain domed cap with a short slanted stalk on top, over a
smooth egg-shaped nut that tapers to a blunt point at the bottom. The
cap overhangs the nut and is parted from it by a thin standing line."""

from shapely import affinity
from shapely.geometry import Point, Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

CAP_W, CAP_H = 20.0, 7.6  # the dome is the top half of an ellipse this wide and twice this tall
CAP_RIM = 2.0  # v of the cap's flat underside
CAP_ROUND = 1.6  # rounds the rim's corners
STALK = [(0.0, CAP_RIM + CAP_H - 1.0), (1.8, CAP_RIM + CAP_H + 2.0)]  # slanted stub on the crown
STALK_W = 2.6
SEAM = 1.2  # standing line between cap and nut
NUT_W, NUT_TOP, NUT_BOTTOM = 16.5, CAP_RIM - SEAM, -13.5  # the nut is widest just under the cap and tapers to its tip
NUT_ROUND = 2.2  # blunts the tip
SMOOTH = 3
CLOSE = 0.8  # blends the stalk into the cap


def _smooth(points, rounds):
    """Chaikin corner cutting on a closed ring."""
    for _ in range(rounds):
        cut = []
        for (u0, v0), (u1, v1) in zip(points, points[1:] + points[:1]):
            cut.append((0.75 * u0 + 0.25 * u1, 0.75 * v0 + 0.25 * v1))
            cut.append((0.25 * u0 + 0.75 * u1, 0.25 * v0 + 0.75 * v1))
        points = cut
    return points


def draw():
    dome = affinity.scale(Point(0, CAP_RIM).buffer(1.0, 64), CAP_W / 2, CAP_H, origin=(0, CAP_RIM))
    cap = dome.intersection(box(-CAP_W, CAP_RIM, CAP_W, CAP_RIM + CAP_H + 1)).buffer(-CAP_ROUND, 16).buffer(CAP_ROUND, 16)
    cap = union(cap, stroke(STALK, STALK_W)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    half = NUT_W / 2
    mid = (NUT_TOP + NUT_BOTTOM) / 2
    # the nut is drawn a little taller than its top so the smoothing leaves a square shoulder under the cap, then clipped
    egg = [(-half, NUT_TOP + 3.0), (half, NUT_TOP + 3.0), (half, mid + 1.0), (half * 0.55, NUT_BOTTOM + 2.0), (0, NUT_BOTTOM), (-half * 0.55, NUT_BOTTOM + 2.0), (-half, mid + 1.0)]
    nut = Polygon(_smooth(egg, SMOOTH)).intersection(box(-NUT_W, NUT_BOTTOM - 1, NUT_W, NUT_TOP))
    nut = nut.buffer(-NUT_ROUND, 16).buffer(NUT_ROUND, 16)
    return union(cap, nut)


motif = Motif(name="acorn", issue=126, draw=draw)
