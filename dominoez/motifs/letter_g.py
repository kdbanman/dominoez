"""A bold geometric capital G, hand-built from strokes rather than a font
glyph. A thick circular arc forms the bowl, open on the upper right; the
arc's lower-right quadrant already reads as the letter's stem, and a
crossbar runs inward from where the arc ends, at mid-height, toward the
centre, giving the letter its characteristic notch."""

import math

from ..geometry import stroke, union
from ..motif import Motif

RADIUS = 8.5  # centreline radius of the bowl's arc
STROKE = 4.5  # width of every stroke: bold, logo-like
BAR_INSET = 7.0  # crossbar length, running left from the bowl's end at (RADIUS, 0)
TOP_ANGLE = 50.0  # degrees; where the arc's upper terminal starts, above the opening
ARC_POINTS = 80  # samples along the bowl's arc, for a smooth curve


def _arc(r: float, a_start: float, a_end: float, n: int) -> list[tuple[float, float]]:
    """Points along a circle of radius r, from a_start to a_end degrees (ccw)."""
    return [
        (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))
        for a in [a_start + (a_end - a_start) * i / (n - 1) for i in range(n)]
    ]


def draw():
    # Bowl: the arc sweeps counterclockwise from the upper-right terminal,
    # through the top, left and bottom, ending at mid-height on the right
    # (R, 0). The short way, from there back up to the terminal, is the
    # opening. The arc's own lower-right quadrant (270 to 360) is the stem;
    # nothing is added past the bowl's right edge.
    bowl = stroke(_arc(RADIUS, TOP_ANGLE, 360.0, ARC_POINTS), STROKE)
    # Crossbar: from the bowl's end, straight inward toward the centre, flat
    # caps so the join with the bowl is a crisp notch rather than a rounded
    # blob. Its left end stops short of the centreline.
    bar = stroke([(RADIUS, 0.0), (RADIUS - BAR_INSET, 0.0)], STROKE, cap="flat")
    g = union(bowl, bar)
    # Close the thin sliver where the straight bar meets the curved bowl.
    return g.buffer(0.6, 16).buffer(-0.6, 16)


motif = Motif(name="letter_g", issue=4, draw=draw)
