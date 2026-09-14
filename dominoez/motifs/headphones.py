"""Over-ear headphones, front on, as a flat icon: a thick padded headband
arching over the top, sitting just above a thin frame that arches under it
and continues down both sides to the ear cups. The cups are big plump eggs,
narrow end up and leaning inward, hanging inside the frame's legs with their
outer edges running on from the legs. Symmetric about the centreline; no
driver dots."""

import math

from shapely import affinity
from shapely.geometry import LineString, Polygon

from ..geometry import stroke, union
from ..motif import Motif

FRAME_C = (0.0, -4.2)  # centre of the frame's arch, an ellipse arc
FRAME_A, FRAME_B = 10.2, 9.2  # centreline semi-axes of the arch, across and up
FRAME_END = -30.0  # degrees below horizontal where each leg of the arch ends, curving inward, inside its cup
FRAME_W = 1.6
BAND_SPAN = (43.0, 137.0)  # degrees of the arch the padded band sits over; shorter than the arch
BAND_W = 4.0
BAND_GAP = 1.2  # standing wall between the frame and the band
CUP_R, CUP_TOP = 3.8, 5.6  # the egg is a semicircle of radius CUP_R below its equator and a half ellipse CUP_TOP tall above it
CUP_TILT = 18.0  # degrees the cup's tip leans toward the centre
CLOSE = 0.6  # rounds the crease where each frame leg meets its cup without filling the notch above it


def _arch_pts(a0, a1, steps=96):
    return [
        (FRAME_C[0] + FRAME_A * math.cos(math.radians(a)), FRAME_C[1] + FRAME_B * math.sin(math.radians(a)))
        for a in [a0 + (a1 - a0) * i / steps for i in range(steps + 1)]
    ]


def _frame():
    return stroke(_arch_pts(FRAME_END, 180.0 - FRAME_END), FRAME_W)


def _band():
    # A parallel to the arch, offset outward so the gap to the frame is constant along the band.
    # The arch runs counter-clockwise, so outward is a negative offset.
    line = LineString(_arch_pts(*BAND_SPAN)).offset_curve(-(FRAME_W / 2 + BAND_GAP + BAND_W / 2))
    return line.buffer(BAND_W / 2, 32)


def _cup():
    """The right cup. Its round bottom is tangent to the frame's outer edge where the leg
    ends, so the leg's outline runs straight on into the cup's."""
    pts = []
    for i in range(128):
        t = 2 * math.pi * i / 128
        pts.append((CUP_R * math.cos(t), (CUP_TOP if math.sin(t) > 0 else CUP_R) * math.sin(t)))
    egg = Polygon(pts)
    t = math.radians(FRAME_END)
    end = _arch_pts(FRAME_END, FRAME_END, 1)[0]
    nx, ny = FRAME_B * math.cos(t), FRAME_A * math.sin(t)  # outward normal of the ellipse at the end
    n = math.hypot(nx, ny)
    centre = (end[0] - nx / n * (CUP_R - FRAME_W / 2), end[1] - ny / n * (CUP_R - FRAME_W / 2))
    return affinity.translate(affinity.rotate(egg, CUP_TILT, origin=(0, 0)), *centre)


def _mirror(g):
    return affinity.scale(g, -1.0, 1.0, origin=(0, 0))


def draw():
    cup = _cup()
    frame = union(_frame(), cup, _mirror(cup)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(frame, _band())


motif = Motif(name="headphones", issue=37, draw=draw)
