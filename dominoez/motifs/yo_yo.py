"""A yo-yo mid-drop, face on: a big cut disc with a standing ring inside
for the hub, and its string peeling off the top of the disc, running up
and to the right to a finger loop. The string leans because a loop
straight above a disc this heavy would leave the box."""

from shapely.geometry import Point

from ..geometry import stroke, union
from ..motif import Motif

DISC_C = (-3.0, -3.0)
DISC_R = 7.6
HUB_R = (4.0, 5.6)  # inner and outer radius of the standing ring inside the disc, 1.6 wide
STRING = [(-3.0, 3.6), (-0.5, 4.5), (3.0, 5.6), (5.8, 7.4), (7.6, 9.2)]  # from the top of the disc, tangent at first, then up to the loop
STRING_W = 2.2
LOOP_C = (9.0, 10.6)
LOOP_R = (1.4, 3.2)  # inner (standing) and outer radius of the finger loop
SPLINE_STEPS = 6  # points per segment when the string's control points are smoothed
CLOSE = 0.8  # fills the creases where the string meets the disc and the loop


def _spline(points):
    """A Catmull-Rom curve through the points, so the string reads as a curve."""
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
    disc = Point(*DISC_C).buffer(DISC_R, 96)
    hub = Point(*DISC_C).buffer(HUB_R[1], 64).difference(Point(*DISC_C).buffer(HUB_R[0], 64))
    loop = Point(*LOOP_C).buffer(LOOP_R[1], 48).difference(Point(*LOOP_C).buffer(LOOP_R[0], 48))
    yo = union(disc, stroke(_spline(STRING), STRING_W), loop).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return yo.difference(hub)


motif = Motif(name="yo_yo", issue=136, draw=draw)
