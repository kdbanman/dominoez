"""A pair of eyeglasses seen front on: two round lens frames joined by an
arched bridge, with a short arm stub leaving each outer edge. The lenses
themselves stay standing, so the frames read as rings."""

from ..geometry import dot, stroke, union
from ..motif import Motif

LENS_C = (6.0, 0.0)  # right lens centre; the left is mirrored
LENS_R = 5.2  # outer radius of the frame
FRAME_W = 2.0  # the cut ring
BRIDGE = [(-2.2, 1.6), (0.0, 2.6), (2.2, 1.6)]  # arches up between the rings
BRIDGE_W = 1.8
ARM = [(10.8, 1.2), (12.8, 2.4)]  # right arm stub, ring outward; the left is mirrored
ARM_W = 1.8
CLOSE = 0.6  # rounds the creases where the bridge and arms meet the rings


def _mirror(points):
    return [(-u, v) for u, v in points]


def _ring(u, v):
    return dot(u, v, 2 * LENS_R).difference(dot(u, v, 2 * (LENS_R - FRAME_W)))


def draw():
    rings = union(_ring(*LENS_C), _ring(-LENS_C[0], LENS_C[1]))
    frame = union(rings, stroke(BRIDGE, BRIDGE_W), stroke(ARM, ARM_W), stroke(_mirror(ARM), ARM_W))
    return frame.buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="glasses", issue=41, draw=draw)
