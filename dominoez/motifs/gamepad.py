"""A gamepad silhouette: a rounded body with two grips hanging down, a
standing d-pad on the left and four standing buttons in a diamond on the
right."""

from shapely.geometry import box

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif
from shapely import affinity

BODY = (22.0, 9.5, 2.5)  # width, height, corner radius
BODY_C = (0.0, 2.25)
GRIP = [(-7.5, 3.0), (-10.0, -6.0)]  # left grip centreline, top to bottom; the right is mirrored
GRIP_W = 6.5
DPAD_C = (-6.5, 2.25)
DPAD_LEN, DPAD_W = 5.5, 2.0  # standing plus
BUTTONS_C = (6.5, 2.25)
BUTTON_SPREAD = 2.4  # centre to each button
BUTTON_D = 1.9
ROUND = 0.8  # blunts the d-pad's corners, past half the island minimum
CLOSE = 0.6  # rounds the creases where the grips leave the body


def _mirror(points):
    return [(-u, v) for u, v in points]


def draw():
    body = affinity.translate(rounded_rect(*BODY), *BODY_C)
    grips = [stroke(GRIP, GRIP_W), stroke(_mirror(GRIP), GRIP_W)]
    pad = union(body, *grips).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    cu, cv = DPAD_C
    h = DPAD_LEN / 2
    dpad = union(
        box(cu - h, cv - DPAD_W / 2, cu + h, cv + DPAD_W / 2),
        box(cu - DPAD_W / 2, cv - h, cu + DPAD_W / 2, cv + h),
    ).buffer(-ROUND, 8).buffer(ROUND, 8)
    bu, bv = BUTTONS_C
    s = BUTTON_SPREAD
    buttons = [dot(bu, bv + s, BUTTON_D), dot(bu, bv - s, BUTTON_D), dot(bu - s, bv, BUTTON_D), dot(bu + s, bv, BUTTON_D)]
    return pad.difference(union(dpad, *buttons))


motif = Motif(name="gamepad", issue=17, draw=draw)
