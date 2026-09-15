"""A wood hand saw, side view, handle on the left: a closed D-handle with a
standing grip opening, and a long blade tapering to the right with a row of
blunt teeth along its lower edge."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, union
from ..motif import Motif

HANDLE = (8.0, 11.0, 3.5)  # width, height, corner radius
HANDLE_C = (-8.5, 0.5)
GRIP = (3.2, 5.5, 1.4)  # standing opening in the handle, past the island minimum
GRIP_C = (-8.5, 0.2)
HEEL_TOP, HEEL_BOTTOM = (-5.5, 5.5), (-5.5, -2.5)  # blade edge at the handle
TOE_TOP, TOE_BOTTOM = (12.0, 2.0), (12.0, -0.2)  # blade edge at the tip
TEETH = 6
TOOTH_DEPTH = 2.0
BLUNT = 0.5  # opening radius that rounds each tooth tip past the channel minimum


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _blade():
    edge = [HEEL_BOTTOM]
    for i in range(TEETH):
        u_tip, v_tip = _lerp(HEEL_BOTTOM, TOE_BOTTOM, (i + 0.5) / TEETH)
        edge.append((u_tip, v_tip - TOOTH_DEPTH))
        edge.append(_lerp(HEEL_BOTTOM, TOE_BOTTOM, (i + 1) / TEETH))
    blade = Polygon([HEEL_TOP, *edge, TOE_TOP])
    return blade.buffer(-BLUNT, 8).buffer(BLUNT, 8)


def draw():
    handle = affinity.translate(rounded_rect(*HANDLE), *HANDLE_C)
    grip = affinity.translate(rounded_rect(*GRIP), *GRIP_C)
    return union(handle, _blade()).difference(grip)


motif = Motif(name="saw", issue=44, draw=draw)
