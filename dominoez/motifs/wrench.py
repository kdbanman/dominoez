"""An open-end wrench leaning to the right: a round head with an angled
open jaw at the top, a fat shaft and a rounded knob at the far end."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import rounded_rect, union
from ..motif import Motif

HEAD_C = (0.0, 9.0)
HEAD_R = 6.0
JAW = (4.4, 9.0, 1.0)  # the standing opening: width, length, corner radius
JAW_C = (1.6, 12.6)  # its centre, so it opens out of the head's top right
JAW_ANGLE = -20.0  # degrees, the jaw is angled off the shaft like a real wrench
SHAFT = [(-2.5, 9.0), (2.5, 9.0), (2.2, -12.0), (-2.2, -12.0)]  # slightly narrower toward the far end
KNOB_C = (0.0, -12.2)
KNOB_R = 2.5  # rounded end of the shaft, a little fuller than the shaft
TILT = -30.0  # degrees, so the head leans right
CLOSE = 1.0  # blends the shaft into the head and the knob
ROUND = 0.5


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    knob = Point(*KNOB_C).buffer(KNOB_R, 32)
    wrench = union(head, Polygon(SHAFT), knob).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    jaw = affinity.translate(affinity.rotate(rounded_rect(*JAW), JAW_ANGLE, origin=(0, 0)), *JAW_C)
    return affinity.rotate(wrench.difference(jaw), TILT, origin=(0, 0))


motif = Motif(name="wrench", issue=140, draw=draw)
