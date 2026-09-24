"""The classic lightning bolt: a wide top, a sharp jag to the right in the
middle, and a long narrowing tail down to a point at the bottom left.
One solid silhouette with blunted corners."""

from shapely import affinity
from shapely.geometry import Polygon

from ..motif import Motif

# The outline, clockwise from the top left corner
BOLT = [
    (-7.5, 14.0),  # top left
    (4.5, 14.0),  # top right
    (0.0, 3.5),  # inside of the jag, upper
    (8.0, 3.5),  # the jag's point
    (-6.0, -14.0),  # the tip
    (-1.5, -2.5),  # inside of the jag, lower
    (-9.5, -2.5),  # the notch on the left
]
ROUND = 0.8  # blunts the tip and corners
SCALE = 1.15  # the outline is laid out small and grown to fill the box's height


def draw():
    bolt = Polygon(BOLT).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(bolt, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="lightning_bolt", issue=129, draw=draw)
