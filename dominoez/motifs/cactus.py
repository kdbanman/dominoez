"""A saguaro cactus in a pot: one fat upright trunk with a rounded top,
two arms of the same fat stroke reaching out and turning up at different
heights, the left one lower than the right, and a plain pot below, a rim
band over a tapered body, parted from it by a thin standing line."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

TRUNK_W, TRUNK_BOTTOM, TRUNK_TOP = 7.2, -8.0, 12.0  # the trunk stands from the pot rim to its rounded crown
ARM_W = 5.0
LEFT_ARM = [(-2.0, 0.5), (-8.8, 0.5), (-8.8, 6.5)]  # out from the trunk, then up; the low arm
RIGHT_ARM = [(2.0, 4.0), (9.0, 4.0), (9.0, 10.0)]  # the high arm
RIM_W, RIM_H, RIM_V = 17.5, 3.4, -9.7  # the pot's rim band, centred at RIM_V
RIM_ROUND = 1.0
SEAM = 1.2  # standing line between rim and pot body
POT_TOP_HALF, POT_BOTTOM_HALF = 7.2, 5.6  # the body tapers to its foot
POT_BOTTOM = -18.0
POT_ROUND = 1.4  # rounds the foot's corners
CLOSE = 0.9  # blends the arms into the trunk and the trunk onto the rim
ROUND = 0.5  # blunts every corner
SCALE = 0.93  # laid out big, then shrunk so the crown stays inside the box


def draw():
    trunk = affinity.translate(rounded_rect(TRUNK_W, TRUNK_TOP - TRUNK_BOTTOM, TRUNK_W / 2), 0, (TRUNK_TOP + TRUNK_BOTTOM) / 2)
    arms = union(stroke(LEFT_ARM, ARM_W), stroke(RIGHT_ARM, ARM_W))
    rim = affinity.translate(rounded_rect(RIM_W, RIM_H, RIM_ROUND), 0, RIM_V)
    plant = union(trunk, arms, rim).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    pot_top = RIM_V - RIM_H / 2 - SEAM
    pot = Polygon([(-POT_TOP_HALF, pot_top), (POT_TOP_HALF, pot_top), (POT_BOTTOM_HALF, POT_BOTTOM), (-POT_BOTTOM_HALF, POT_BOTTOM)])
    pot = pot.buffer(-POT_ROUND, 16).buffer(POT_ROUND, 16)
    cactus = union(plant, pot).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(cactus, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="cactus", issue=121, draw=draw)
