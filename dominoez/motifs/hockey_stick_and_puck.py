"""An ice hockey stick and puck: a fat shaft leaning from the top left
down to the right into a rectangular blade lying along the ice, meeting
it in a plain mitre at the heel, and a flat puck side-on, sliding away
behind the heel."""

from shapely import affinity

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

BLADE = (10.0, 4.6, 0.8)  # width, height, corner radius of the blade
BLADE_C = (6.5, -9.2)
BLADE_ANGLE = -14.0  # degrees, the blade tips down a little toward the toe
SHAFT = [(-9.4, 7.0), (2.6, -9.2)]  # top of the shaft to a point inside the blade's heel, so the shaft covers the heel end
SHAFT_W = 3.8
PUCK = (8.0, 3.2, 1.3)  # width, height, corner radius of the puck seen side-on
PUCK_C = (-6.6, -10.9)
CLOSE = 0.3  # a hair of closing at the mitre only, so the heel keeps its plain angle
ROUND = 0.5  # blunts the shaft's top corners and any sliver at the heel


def draw():
    blade = affinity.translate(affinity.rotate(rounded_rect(*BLADE), BLADE_ANGLE, origin=(0, 0)), *BLADE_C)
    stick = union(stroke(SHAFT, SHAFT_W, cap="flat"), blade)
    stick = stick.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    puck = affinity.translate(rounded_rect(*PUCK), *PUCK_C)
    return union(stick, puck)


motif = Motif(name="hockey_stick_and_puck", issue=133, draw=draw)
