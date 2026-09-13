"""A Lego brick seen front on: a wide rectangular body with a row of four
studs standing up from its top edge, the way a 2x4 brick looks from the
side."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import rounded_rect, union
from ..motif import Motif

BODY = (22.0, 10.0, 0.8)  # width, height, corner radius
BODY_C = (0.0, -2.0)
STUD_W, STUD_H = 3.6, 2.8  # each stud's width and how far it stands above the body
STUD_PITCH = 5.5  # centre to centre; leaves a wall past the minimum between studs
STUDS = 4
STUD_ROUND = 0.6  # rounds the studs' top corners
STUD_ROOT = 1.0  # how far each stud reaches into the body so the two merge


def draw():
    body = affinity.translate(rounded_rect(*BODY), *BODY_C)
    top = BODY_C[1] + BODY[1] / 2
    studs = []
    for i in range(STUDS):
        cu = (i - (STUDS - 1) / 2) * STUD_PITCH
        stud = box(cu - STUD_W / 2, top - STUD_ROOT, cu + STUD_W / 2, top + STUD_H)
        studs.append(stud.buffer(-STUD_ROUND, 8).buffer(STUD_ROUND, 8))
    return union(body, *studs)


motif = Motif(name="lego_brick", issue=49, draw=draw)
