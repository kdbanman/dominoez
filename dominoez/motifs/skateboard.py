"""A skateboard seen from the side, facing right: a fat deck with both ends
kicked up, the tail a little steeper than the nose, riding on two oversized
wheels with standing hubs, each hung from the deck on a short truck."""

from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

DECK = [(-11.5, 2.5), (-9.0, -1.0), (9.0, -1.0), (11.5, 1.5)]  # kicked tail at the left, nose at the right
DECK_W = 4.0
WHEELS = [(-6.5, -8.0), (6.5, -8.0)]
WHEEL_R = 3.8  # oversized
HUB_D = 2.0  # standing
TRUCKS = [[(-6.5, -1.0), (-6.5, -5.0)], [(6.5, -1.0), (6.5, -5.0)]]
TRUCK_W = 2.8
CLOSE = 1.5  # smooths the deck's bends and the truck joints
ROUND = 0.5


def draw():
    board = union(stroke(DECK, DECK_W), *(stroke(t, TRUCK_W) for t in TRUCKS))
    board = board.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    wheels = [Point(*c).buffer(WHEEL_R, 48).difference(dot(*c, HUB_D)) for c in WHEELS]
    return union(board, *wheels)


motif = Motif(name="skateboard", issue=105, draw=draw)
