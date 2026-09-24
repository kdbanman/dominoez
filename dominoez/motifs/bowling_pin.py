"""A bowling pin, upright, as one silhouette: a round belly low down, a
long pronounced neck and a small domed head, with two standing stripes
across the neck. The outline is a mirrored profile smoothed into a
curve, laid out 26 mm tall and scaled down only as far as the box needs."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..motif import Motif

# The right half of the outline, (r, v), from the foot up to the crown; the left half is its mirror.
# 26 mm tall: belly 12 mm wide at 35 percent of the height, neck 4.4 mm at 70 percent, head 6.6 mm with a domed crown.
# The smoothing pulls the curve in a touch, so the widths are drawn a little over.
PROFILE = [
    (0.0, -13.0), (3.0, -13.0), (4.6, -11.5), (5.7, -8.5), (6.15, -5.5), (6.15, -3.0), (5.5, -0.5), (4.3, 2.0),
    (3.0, 3.8), (2.3, 5.2), (2.4, 6.6), (3.0, 8.0), (3.4, 9.6), (3.2, 11.3), (2.0, 12.6), (0.0, 13.0),
]
SMOOTH = 3  # rounds of corner cutting, so the profile reads as a curve
ROUND = 0.6  # blunts the foot corners
CLOSE = 0.6  # smooths the belly
SCALE = 0.9  # the pin is bottom-heavy; the smallest uniform shrink that keeps the crown within 14 mm of the centroid
NECK_V = 5.9  # v of the neck's middle before scaling; the stripes sit either side of it
STRIPE_H = 1.6  # standing, above the wall minimum
BAND = 2.0  # cut band between the two stripes
HALF_W = 8.0  # stripes run clear across the pin


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
    right = PROFILE
    left = [(-r, v) for r, v in reversed(PROFILE[1:-1])]
    pin = Polygon(_smooth(right + left, SMOOTH))
    pin = pin.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    pin = affinity.scale(pin, SCALE, SCALE, origin=(0, 0))
    for s in (-1, 1):
        v = NECK_V * SCALE + s * (STRIPE_H + BAND) / 2
        pin = pin.difference(box(-HALF_W, v - STRIPE_H / 2, HALF_W, v + STRIPE_H / 2))
    return pin


motif = Motif(name="bowling_pin", issue=134, draw=draw)
