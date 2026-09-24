"""A farm tractor seen from the side, facing right: a huge back wheel and a
small front wheel, both with standing hubs and a wall of air over the tyre,
a tall cab at the back with one standing window, a long low hood in front
and a fat exhaust stack rising from it."""

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

BACK = (-6.0, -6.5)
BACK_R = 6.5
FRONT = (8.5, -8.8)
FRONT_R = 4.2
HUB_BACK, HUB_FRONT = 3.2, 2.4  # standing hub diameters
AIR = 1.2  # wall of air between tyre and body
CHASSIS = (-6.0, -6.5, 10.0, -2.0)  # (u0, v0, u1, v1)
HOOD_W, HOOD_H, HOOD_C = 11.0, 5.0, (6.5, 0.0)  # long low engine cover
CAB_W, CAB_H, CAB_C = 9.0, 12.0, (-3.5, 3.0)  # tall cab
WINDOW_W, WINDOW_H, WINDOW_C = 5.4, 5.0, (-3.0, 5.4)  # standing
STACK = [(4.5, 2.0), (4.5, 8.0)]  # exhaust pipe centreline
STACK_W = 2.4
ROUND = 0.7  # blunts corners and tips
CLOSE = 1.0  # blends hood, cab and chassis


def draw():
    body = union(
        box(*CHASSIS),
        affinity.translate(rounded_rect(HOOD_W, HOOD_H, 1.8), *HOOD_C),
        affinity.translate(rounded_rect(CAB_W, CAB_H, 1.8), *CAB_C),
        stroke(STACK, STACK_W),
    )
    body = body.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    for (u, v), r in ((BACK, BACK_R), (FRONT, FRONT_R)):
        body = body.difference(Point(u, v).buffer(r + AIR, 48))
    body = body.buffer(-ROUND, 16).buffer(ROUND, 16)
    window = affinity.translate(rounded_rect(WINDOW_W, WINDOW_H, 1.2), *WINDOW_C)
    body = body.difference(window)
    back = Point(*BACK).buffer(BACK_R, 64).difference(dot(*BACK, HUB_BACK))
    front = Point(*FRONT).buffer(FRONT_R, 48).difference(dot(*FRONT, HUB_FRONT))
    return union(body, back, front)


motif = Motif(name="tractor", issue=102, draw=draw)
