"""A kick scooter seen from the side, facing right: a low deck between two
small wheels with standing hubs, a rear fender curling over the back wheel,
and a fat steering column leaning back from the front wheel to a
handlebar with a grip at each end."""

from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

REAR = (-8.5, -8.0)
FRONT = (8.5, -8.0)
WHEEL_R = 3.5
HUB_D = 2.0  # standing
DECK = [(-7.5, -5.0), (5.5, -5.0)]  # flat deck between the wheels
DECK_W = 3.4
FENDER = [(-6.0, -5.0), (-8.5, -3.5), (-10.5, -5.0)]  # curls back over the rear wheel
FENDER_W = 3.0
COLUMN = [(7.5, -5.0), (4.5, 9.0)]  # leans back toward the rider
COLUMN_W = 3.4
BAR = [(0.0, 9.5), (9.0, 9.5)]  # handlebar
BAR_W = 3.0
GRIPS = [(-0.5, 9.5, 3.8), (9.5, 9.5, 3.8)]  # cut (u, v, diameter)
CLOSE = 1.0  # bridges the joints
ROUND = 0.6


def draw():
    frame = union(
        stroke(DECK, DECK_W),
        stroke(FENDER, FENDER_W),
        stroke(COLUMN, COLUMN_W),
        stroke(BAR, BAR_W),
        *(dot(*g) for g in GRIPS),
    )
    frame = frame.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    wheels = [Point(*c).buffer(WHEEL_R, 48).difference(dot(*c, HUB_D)) for c in (REAR, FRONT)]
    return union(frame, *wheels)


motif = Motif(name="scooter", issue=104, draw=draw)
