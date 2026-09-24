"""A soccer ball, face on, as the classic icon: a cut ring for the ball's
edge, one whole cut pentagon in the middle, five cut seam lines running
out from its corners, and at the end of each seam a cut pentagon at the
rim pointing inward and clipped by the ring, so the standing patches
between read as the ball's five hexagons."""

import math

from shapely.geometry import Point, Polygon

from ..geometry import stroke, union
from ..motif import Motif

BALL_R = 12.0  # outer radius of the ball
RING_W = 2.2  # the cut band along the ball's edge
CENTRE_R = 4.6  # circumradius of the whole centre pentagon, corner up
RIM_R = 4.6  # circumradius of each rim pentagon
RIM_DIST = 12.6  # centre of each rim pentagon from the ball's centre, so its inward corner sits at 8.0
SEAM_W = 1.3  # cut lines from the centre pentagon's corners to the rim pentagons
SEAM = (3.5, 9.0)  # radii the seams run between, starting inside the centre pentagon and ending inside the rim ones
ROUND = 0.4  # blunts the pentagons' corners


def _pentagon(centre, radius, angle):
    """A regular pentagon with one corner at `angle` (degrees) from the centre."""
    pts = []
    for k in range(5):
        a = math.radians(angle + 72 * k)
        pts.append((centre[0] + radius * math.cos(a), centre[1] + radius * math.sin(a)))
    return Polygon(pts)


def draw():
    ball = Point(0, 0).buffer(BALL_R, 96)
    ring = ball.difference(Point(0, 0).buffer(BALL_R - RING_W, 96))
    parts = [ring, _pentagon((0, 0), CENTRE_R, 90)]
    for k in range(5):
        a = 90 + 72 * k  # corner directions of the centre pentagon
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        parts.append(stroke([(SEAM[0] * ca, SEAM[0] * sa), (SEAM[1] * ca, SEAM[1] * sa)], SEAM_W, cap="flat"))
        rim = _pentagon((RIM_DIST * ca, RIM_DIST * sa), RIM_R, a + 180)  # one corner pointing back at the centre
        parts.append(rim.intersection(ball))
    return union(*parts).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="soccer_ball", issue=132, draw=draw)
