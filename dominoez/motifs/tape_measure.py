"""A tape measure, traced from the Material Design Icons "tape-measure"
icon (Templarian/MaterialDesign, svg/tape-measure.svg, Apache 2.0): a
round case with a square lower right corner, a standing disc for the
reel window, a short tab where the tape leaves the case and, below it,
the tape's hooked end. The outlines are the icon's subpaths sampled
into points, centred, in icon units (a 24 unit view box), scaled so the
picture spans 25 mm and filled even-odd so the window stands."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import union
from ..motif import Motif

# The icon's subpaths, centred on the bounding box, y up: the case, the reel window (a hole) and the hook.
CASE = [
    (-3.0, 8.0), (-2.31, 7.97), (-1.63, 7.87), (-0.97, 7.7), (-0.32, 7.47), (0.3, 7.17), (0.89, 6.82), (1.44, 6.41),
    (1.95, 5.95), (2.41, 5.44), (2.82, 4.89), (3.17, 4.3), (3.47, 3.68), (3.7, 3.03), (3.87, 2.37), (3.97, 1.69),
    (4.0, 1.0), (5.0, 1.0), (5.0, -2.0), (4.0, -2.0), (4.0, -6.0), (-3.0, -6.0), (-3.69, -5.97), (-4.37, -5.87),
    (-5.03, -5.7), (-5.68, -5.47), (-6.3, -5.17), (-6.89, -4.82), (-7.44, -4.41), (-7.95, -3.95), (-8.41, -3.44),
    (-8.82, -2.89), (-9.17, -2.3), (-9.47, -1.68), (-9.7, -1.03), (-9.87, -0.37), (-9.97, 0.31), (-10.0, 1.0),
    (-9.97, 1.69), (-9.87, 2.37), (-9.7, 3.03), (-9.47, 3.68), (-9.17, 4.3), (-8.82, 4.89), (-8.41, 5.44),
    (-7.95, 5.95), (-7.44, 6.41), (-6.89, 6.82), (-6.3, 7.17), (-5.68, 7.47), (-5.03, 7.7), (-4.37, 7.87),
    (-3.69, 7.97), (-3.0, 8.0),
]
WINDOW = [
    (-3.0, 5.0), (-3.39, 4.98), (-3.78, 4.92), (-4.16, 4.83), (-4.53, 4.7), (-4.89, 4.53), (-5.22, 4.33), (-5.54, 4.09),
    (-5.83, 3.83), (-6.09, 3.54), (-6.33, 3.22), (-6.53, 2.89), (-6.7, 2.53), (-6.83, 2.16), (-6.92, 1.78), (-6.98, 1.39),
    (-7.0, 1.0), (-6.98, 0.61), (-6.92, 0.22), (-6.83, -0.16), (-6.7, -0.53), (-6.53, -0.89), (-6.33, -1.22),
    (-6.09, -1.54), (-5.83, -1.83), (-5.54, -2.09), (-5.22, -2.33), (-4.89, -2.53), (-4.53, -2.7), (-4.16, -2.83),
    (-3.78, -2.92), (-3.39, -2.98), (-3.0, -3.0), (-2.61, -2.98), (-2.22, -2.92), (-1.84, -2.83), (-1.47, -2.7),
    (-1.11, -2.53), (-0.78, -2.33), (-0.46, -2.09), (-0.17, -1.83), (0.09, -1.54), (0.33, -1.22), (0.53, -0.89),
    (0.7, -0.53), (0.83, -0.16), (0.92, 0.22), (0.98, 0.61), (1.0, 1.0), (0.98, 1.39), (0.92, 1.78), (0.83, 2.16),
    (0.7, 2.53), (0.53, 2.89), (0.33, 3.22), (0.09, 3.54), (-0.17, 3.83), (-0.46, 4.09), (-0.78, 4.33), (-1.11, 4.53),
    (-1.47, 4.7), (-1.84, 4.83), (-2.22, 4.92), (-2.61, 4.98), (-3.0, 5.0),
]
HOOK = [(5.0, -4.0), (10.0, -4.0), (10.0, -6.0), (10.0, -8.0), (8.0, -8.0), (8.0, -6.0), (5.0, -6.0), (5.0, -4.0)]
SCALE = 1.2  # mm per icon unit: the icon is 20 units wide, so the picture spans 24 mm; at 25 the hook reached the box's edge
CLOSE = 0.4  # smooths the sampled circle
ROUND = 0.4  # blunts the corners; the narrowest cut features, the tab and hook, are 2.5 mm so nothing needs thickening first


def draw():
    case = Polygon(CASE).difference(Polygon(WINDOW))
    tape = union(case, Polygon(HOOK))
    tape = affinity.scale(tape, SCALE, SCALE, origin=(0, 0))
    return tape.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="tape_measure", issue=143, draw=draw)
