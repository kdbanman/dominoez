"""A beamed pair of eighth notes in the emoji style: two big round heads,
fat stems rising from their right edges, and a thick beam bouncing up to
the right across the stem tops. Traced from Twemoji's U+1F3B5 musical
note (twitter/twemoji, assets/svg/1f3b5.svg, CC-BY 4.0), sampled from
its cubic beziers and scaled to 24 mm tall."""

from shapely import affinity
from shapely.geometry import Polygon

from ..motif import Motif

# The outline in mm, clockwise from the beam's top right corner, as sampled from the Twemoji path: down the beam's
# right end and the right stem, round the right head, up the right stem's left edge, along the beam's underside,
# up the left stem's right edge, round the left head, up the left stem's left edge and along the beam's top.
OUTLINE = [
    (11.18, 11.99), (-4.28, 10.21), (-4.48, 10.17), (-4.67, 10.1), (-4.85, 10.0), (-5.01, 9.88), (-5.15, 9.74), (-5.28, 9.58),
    (-5.38, 9.41), (-5.45, 9.22), (-5.5, 9.03), (-5.52, 8.82), (-5.52, -4.13), (-5.71, -4.05), (-5.9, -3.99), (-6.1, -3.93),
    (-6.3, -3.88), (-6.51, -3.83), (-6.72, -3.79), (-6.93, -3.76), (-7.15, -3.74), (-7.36, -3.73), (-7.59, -3.72), (-8.37, -3.78),
    (-9.11, -3.94), (-9.8, -4.19), (-10.44, -4.52), (-11.0, -4.94), (-11.48, -5.42), (-11.87, -5.96), (-12.17, -6.55), (-12.35, -7.19),
    (-12.41, -7.86), (-12.35, -8.53), (-12.17, -9.17), (-11.87, -9.76), (-11.48, -10.31), (-11.0, -10.79), (-10.44, -11.2), (-9.8, -11.54),
    (-9.11, -11.79), (-8.37, -11.95), (-7.59, -12.0), (-6.8, -11.95), (-6.06, -11.79), (-5.37, -11.54), (-4.73, -11.2), (-4.17, -10.79),
    (-3.69, -10.31), (-3.3, -9.76), (-3.0, -9.17), (-2.82, -8.53), (-2.76, -7.86), (-2.76, 4.87), (9.65, 6.3), (9.65, -2.75),
    (9.46, -2.68), (9.27, -2.61), (9.07, -2.55), (8.87, -2.5), (8.66, -2.45), (8.45, -2.41), (8.24, -2.38), (8.03, -2.36),
    (7.81, -2.35), (7.59, -2.35), (6.8, -2.4), (6.06, -2.56), (5.37, -2.81), (4.73, -3.14), (4.17, -3.56), (3.69, -4.04),
    (3.3, -4.58), (3.0, -5.18), (2.82, -5.81), (2.76, -6.48), (2.82, -7.15), (3.0, -7.79), (3.3, -8.38), (3.69, -8.93),
    (4.17, -9.41), (4.73, -9.82), (5.37, -10.16), (6.06, -10.41), (6.8, -10.57), (7.59, -10.62), (8.37, -10.57), (9.11, -10.41),
    (9.8, -10.16), (10.44, -9.82), (11.0, -9.41), (11.48, -8.93), (11.87, -8.38), (12.17, -7.79), (12.35, -7.15), (12.41, -6.48),
    (12.41, 10.89), (12.4, 11.09), (12.35, 11.28), (12.27, 11.45), (12.17, 11.6), (12.05, 11.73), (11.91, 11.84), (11.74, 11.92),
    (11.57, 11.97), (11.38, 12.0),
]
CLOSE = 0.5  # smooths the sampled curves and the creases where the stems meet the heads
ROUND = 0.4  # blunts the beam's corners
SCALE = 0.96  # the trace is 24 mm tall; shrunk a little so the left head, 14.4 mm from the centroid at full size, stays inside the box


def draw():
    note = Polygon(OUTLINE).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(note, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="music_note", issue=147, draw=draw)
