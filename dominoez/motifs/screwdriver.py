"""A flat-head screwdriver leaning to the right: a fat rounded handle, a
short collar, a straight shank and a blade that widens to a blunt flat
tip."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

HANDLE = (7.4, 13.0, 2.8)  # width, height, corner radius
HANDLE_C = (0.0, 7.6)
COLLAR = (4.4, 2.6, 0.8)  # narrower band where the shank leaves the handle
COLLAR_C = (0.0, 0.4)
SHANK = [(0.0, 0.8), (0.0, -10.5)]
SHANK_W = 2.6
BLADE = [(-1.3, -10.0), (1.3, -10.0), (2.2, -13.6), (2.2, -14.4), (-2.2, -14.4), (-2.2, -13.6)]  # flares to the flat tip
TILT = -30.0  # degrees, so the handle leans right
SCALE = 1.08  # laid out a touch small, then grown to fill the box
ROUND = 0.5  # blunts the tip's corners
CLOSE = 0.6  # blends the collar into the handle


def draw():
    handle = affinity.translate(rounded_rect(*HANDLE), *HANDLE_C)
    collar = affinity.translate(rounded_rect(*COLLAR), *COLLAR_C)
    tool = union(handle, collar, stroke(SHANK, SHANK_W, cap="flat"), Polygon(BLADE))
    tool = tool.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(affinity.rotate(tool, TILT, origin=(0, 0)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="screwdriver", issue=141, draw=draw)
