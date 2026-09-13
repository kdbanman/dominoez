"""A 2x4 Lego brick seen from directly above: a 2:1 rounded rectangle cut
into the face, with eight round studs left standing in a two by four grid.
Proportions follow the real brick (8 mm stud pitch, 4.8 mm studs, 16 x 32 mm
outline) scaled to fit the face."""

from shapely.geometry import Point

from ..geometry import rounded_rect, union
from ..motif import Motif

PITCH = 6.0  # stud centre to centre; the real brick is 8 mm
COLS, ROWS = 4, 2
BODY_W, BODY_H = PITCH * COLS, PITCH * ROWS  # 24 x 12, the 2:1 outline of a 2x4 brick
BODY_R = 1.6  # corner radius of the outline; rounder than the real brick so it reads as an icon
STUD_D = PITCH * 0.6  # 3.6; the real brick's 4.8 mm studs on an 8 mm pitch
# Between studs: PITCH - STUD_D = 2.4 mm of cut. Stud to outline: 1.2 mm of cut. Both past the 1.0 mm minimum.


def draw():
    body = rounded_rect(BODY_W, BODY_H, BODY_R)
    studs = [
        Point((c - (COLS - 1) / 2) * PITCH, (r - (ROWS - 1) / 2) * PITCH).buffer(STUD_D / 2, 32)
        for c in range(COLS)
        for r in range(ROWS)
    ]
    return body.difference(union(*studs))


motif = Motif(name="lego_brick", issue=49, draw=draw)
