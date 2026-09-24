"""A tulip: one bloom with three pointed petals in a rounded cup, a curved
stem, and two separate smooth leaves, each a pointed lens rising from the
stem's foot and angling up and out, touching the stem only at its base,
the left one longer and higher so the pair is not machined."""

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

# The bloom's outline, counter-clockwise from the left tip: down the left side, round the cup, up the right side, then the two notches and the middle tip
BLOOM = [
    (-8.5, 12.5),  # left tip
    (-8.8, 8.0), (-8.0, 3.5), (-5.0, 0.8), (0.0, 0.0), (5.0, 0.8), (8.0, 3.5), (8.8, 8.0),
    (8.5, 12.5),  # right tip
    (4.6, 7.0),  # right notch
    (0.0, 11.5),  # middle tip
    (-4.6, 7.0),  # left notch
]
CUP_SMOOTH = 2  # rounds of corner cutting on the cup so it is a curve
NOTCH = 0.7  # closing that rounds the notches to a printable width
STEM = [(0.0, 1.0), (0.9, -3.0), (-0.4, -7.0), (0.0, -12.6)]  # curves up top, near vertical past the leaves so their gaps stay open, down to the foot they sprout from
STEM_W = 2.8
LEAF_R = 12.3  # each leaf is a lens, the overlap of two discs of this radius
LEAF_OFFSET = 10.0  # whose centres sit this far either side of the leaf's chord midpoint, so the lens is 4.6 mm wide at its middle
LEFT_LEAF = ((-2.2, -12.8), (-9.8, -2.2))  # (foot, tip): the chord the lens lies along, from beside the stem's foot up and out; starting beside the stem rather than on it keeps the gap above the foot open
RIGHT_LEAF = ((2.2, -12.8), (8.8, -4.2))
FOOT = (0.0, -13.3, 4.4)  # a dot that joins the stem's end and the two leaf bases into one rounded foot (u, v, diameter)
CLOSE = 0.6  # blends the bloom onto the stem and rounds the crease where each leaf leaves the stem; small, so the leaves stay parted from the stem above their bases
ROUND = 0.6  # blunts the tips
SCALE = 0.95  # laid out big, then shrunk so the bloom stays inside the box


def _smooth(points, rounds):
    """Chaikin corner cutting on an open chain; the ends stay put."""
    for _ in range(rounds):
        cut = [points[0]]
        for (u0, v0), (u1, v1) in zip(points, points[1:]):
            cut.append((0.75 * u0 + 0.25 * u1, 0.75 * v0 + 0.25 * v1))
            cut.append((0.25 * u0 + 0.75 * u1, 0.25 * v0 + 0.75 * v1))
        cut.append(points[-1])
        points = cut
    return points


def _leaf(foot, tip):
    """A smooth pointed lens along the chord from foot to tip: the overlap of two equal discs offset across the chord."""
    mu, mv = (foot[0] + tip[0]) / 2, (foot[1] + tip[1]) / 2
    du, dv = tip[0] - foot[0], tip[1] - foot[1]
    length = math.hypot(du, dv)
    nu, nv = -dv / length, du / length  # unit normal to the chord
    a = Point(mu + LEAF_OFFSET * nu, mv + LEAF_OFFSET * nv).buffer(LEAF_R, 96)
    b = Point(mu - LEAF_OFFSET * nu, mv - LEAF_OFFSET * nv).buffer(LEAF_R, 96)
    return a.intersection(b)


def draw():
    # only the cup, from tip to tip, is smoothed; the notches and middle tip stay sharp until the finishing pass
    ring = _smooth(BLOOM[:9], CUP_SMOOTH) + BLOOM[9:]
    bloom = Polygon(ring).buffer(NOTCH, 16).buffer(-NOTCH, 16)
    flower = union(bloom, stroke(STEM, STEM_W), _leaf(*LEFT_LEAF), _leaf(*RIGHT_LEAF), dot(*FOOT))
    flower = flower.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(flower, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="tulip", issue=123, draw=draw)
