"""A snare drum seen from a little above, tilted a few degrees: a wide
shell with the head as an ellipse on top, its front rim marked by a
standing arc, and two drumsticks crossed on the head, their handles
reaching up and out."""

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

SHELL_W, SHELL_H, SHELL_C = 25.2, 10.5, (0.0, -4.25)  # the drum's side, a box rounded at the bottom and square at the top where the head sits on it
SHELL_ROUND = 1.8
HEAD_W, HEAD_H, HEAD_C = 25.2, 7.0, (0.0, 1.0)  # the head, an ellipse on top of the shell, as wide as it so the rim arc runs out clean at the corners
RIM_W = 1.2  # standing arc along the head's front edge
STICKS = [[(-8.2, 9.5), (5.0, 0.5)], [(8.2, 9.5), (-5.0, 0.5)]]  # crossed at the head's far edge, handles up and out
STICK_W = 2.3
TILT = 12.0  # degrees counter-clockwise
CLOSE = 0.9  # fills the crease where the sticks cross above the head
ROUND = 0.5


def _head():
    return affinity.scale(Point(*HEAD_C).buffer(1.0, 96), HEAD_W / 2, HEAD_H / 2, origin=HEAD_C)


def draw():
    shell = affinity.translate(rounded_rect(SHELL_W, SHELL_H, SHELL_ROUND), *SHELL_C)
    shell = union(shell, box(-SHELL_W / 2, SHELL_C[1] - SHELL_H / 2 + SHELL_ROUND, SHELL_W / 2, SHELL_C[1] + SHELL_H / 2))  # square top corners
    head = _head()
    sticks = union(*(stroke(s, STICK_W) for s in STICKS))
    drum = union(shell, head, sticks).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    # the front half of the head's edge stands as the rim, subtracted after the finishing so it keeps its width
    front = head.exterior.buffer(RIM_W / 2).intersection(box(-HEAD_W, HEAD_C[1] - HEAD_H, HEAD_W, HEAD_C[1]))
    drum = drum.difference(front).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.rotate(drum, TILT, origin=(0, 0))


motif = Motif(name="drum", issue=146, draw=draw)
