"""A claw hammer, traced from the Material Design Icons "hammer" icon
(Templarian/MaterialDesign, svg/hammer.svg, Apache 2.0): the head at
the top right with a rounded striking face and a split claw, on a
straight handle running down to the bottom left at forty-five degrees.
The outline is the icon's path sampled into points, centred, in icon
units (a 24 unit view box), and scaled so the picture spans 25 mm."""

from shapely import affinity
from shapely.geometry import Polygon

from ..motif import Motif

# The icon's single closed path, centred on its bounding box, y up. Straight edges are the icon's own
# corners; the striking face's curve is sampled at 16 points.
OUTLINE = [
    (-10.0, -7.25), (1.43, 4.18), (0.72, 4.88), (2.14, 6.31), (0.0, 8.49), (0.23, 8.7), (0.48, 8.88), (0.74, 9.03),
    (1.01, 9.16), (1.28, 9.26), (1.57, 9.33), (1.85, 9.37), (2.14, 9.38), (2.43, 9.37), (2.72, 9.33), (3.0, 9.26),
    (3.27, 9.16), (3.54, 9.03), (3.8, 8.88), (4.04, 8.7), (4.27, 8.49), (7.87, 4.88), (6.45, 3.47), (9.29, 3.47),
    (10.0, 2.76), (6.45, -0.83), (5.74, -0.12), (5.74, 2.76), (4.27, 1.34), (3.56, 2.05), (-7.87, -9.38), (-10.0, -7.25),
]
SCALE = 1.25  # mm per icon unit: the icon is 20 units wide, so the hammer spans 25 mm
CLOSE = 0.4  # smooths the sampled curve and the inside corners
ROUND = 0.4  # blunts the tips; the narrowest feature, the claw's lower prong, is 1.25 mm so nothing needs thickening first


def draw():
    hammer = affinity.scale(Polygon(OUTLINE), SCALE, SCALE, origin=(0, 0))
    return hammer.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="hammer", issue=139, draw=draw)
