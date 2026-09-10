"""A bicycle seen from the side, facing right. Two ringed wheels with axle
dots, a diamond frame in fat strokes, a saddle and a handlebar."""

from shapely.geometry import Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

WHEEL_R = 5.4  # outer radius of each wheel
RIM_W = 2.0  # the cut ring that is the tyre
HUB_D = 2.0  # cut dot at each axle
REAR = (-8.2, -4.5)
FRONT = (8.2, -4.5)
BOTTOM_BRACKET = (0.0, -4.0)
SEAT = (-4.2, 5.0)  # top of the seat tube
HEAD_TOP = (5.0, 5.2)  # where the top tube meets the head tube
HEAD_BOTTOM = (6.3, 1.5)  # where the down tube meets the head tube
STEM_TOP = (4.1, 8.8)
BAR = [(4.1, 8.8), (7.5, 8.7), (8.8, 7.2)]
SADDLE = [(-7.0, 8.8), (-2.8, 8.8)]
TUBE_W = 1.6
BAR_W = 1.6
SADDLE_W = 2.2
DROPOUT = 4.0  # length of the solid wedge where the stays meet the rear hub
CLOSE = 0.8  # rounds standing tips past half the island minimum, below half any gap


def _wheel(centre):
    return dot(*centre, 2 * WHEEL_R).difference(dot(*centre, 2 * (WHEEL_R - RIM_W)))


def _toward(a, b, length):
    du, dv = b[0] - a[0], b[1] - a[1]
    n = (du**2 + dv**2) ** 0.5
    return (a[0] + du * length / n, a[1] + dv * length / n)


def draw():
    tubes = [
        [BOTTOM_BRACKET, SEAT],
        [SEAT, HEAD_TOP],
        [BOTTOM_BRACKET, HEAD_BOTTOM],
        [HEAD_BOTTOM, HEAD_TOP, STEM_TOP],
        [HEAD_BOTTOM, FRONT],
        [BOTTOM_BRACKET, REAR],
        [SEAT, REAR],
        [SEAT, (-4.8, 8.8)],
    ]
    dropout = Polygon([REAR, _toward(REAR, BOTTOM_BRACKET, DROPOUT), _toward(REAR, SEAT, DROPOUT)])
    bike = union(
        _wheel(REAR),
        _wheel(FRONT),
        dropout,
        *(stroke(t, TUBE_W) for t in tubes),
        stroke(BAR, BAR_W),
        stroke(SADDLE, SADDLE_W),
    )
    bike = bike.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(bike, dot(*REAR, HUB_D), dot(*FRONT, HUB_D))


motif = Motif(name="bicycle", issue=6, draw=draw)
