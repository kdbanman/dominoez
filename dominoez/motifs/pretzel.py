"""A soft pretzel: one fat rope looped into the classic knot. The rope
rises from an end pressed onto the bottom of the loop, crosses itself in
the middle, curls over the top lobe on that side, comes down the outside
and round the bottom, up the other side, over the other lobe and back
through the crossing to the other end."""

from shapely.geometry import LineString

from ..geometry import stroke
from ..motif import Motif

# One half of the rope, from the left end up through the crossing, over the right lobe and down to the bottom centre.
# The other half is its mirror, so the rope runs: left end, crossing, right lobe, right side, bottom, left side, left lobe, crossing, right end.
HALF = [
    (-6.5, -9.6),  # left end, pressed on the bottom of the loop
    (-3.8, -6.0),
    (0.0, -1.0),  # the crossing
    (3.2, 3.5),
    (6.5, 6.5),
    (10.0, 5.5),
    (11.6, 1.5),
    (11.3, -4.5),
    (8.5, -9.5),
    (4.0, -12.0),
    (0.0, -12.6),  # bottom centre
]
ROPE_W = 4.5
SPLINE_STEPS = 8  # points per segment when the control points are smoothed into a curve
CLOSE = 1.2  # fills the creases at the crossing and where the ends meet the loop


def _path():
    mirror = [(-u, v) for u, v in reversed(HALF)]
    return HALF + mirror[1:]


def _spline(points):
    """A Catmull-Rom curve through the points, so the lobes are round rather than faceted."""
    pts = [points[0], *points, points[-1]]
    out = []
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        for s in range(SPLINE_STEPS):
            t = s / SPLINE_STEPS
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[k]) + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)
                for k in range(2)
            ))
    out.append(points[-1])
    return out


def draw():
    rope = stroke(_spline(_path()), ROPE_W)
    return rope.buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="pretzel", issue=118, draw=draw)
