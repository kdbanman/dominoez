"""A road bike seen from the side, facing right. Two ringed wheels with axle
dots, a diamond frame in fat strokes, a saddle and a drop handlebar.

Proportions follow a real 56 cm road bike scaled to the motif box width:
wheelbase 2.9 wheel radii, saddle and bars about 1.8 radii above the
axles, bottom bracket a little below them."""

from shapely.geometry import Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

WHEEL_R = 5.4  # outer radius of each wheel
RIM_W = 2.0  # the cut ring that is the tyre
HUB_D = 2.0  # cut dot at each axle
REAR = (-8.2, -4.5)
FRONT = (8.2, -4.5)
BOTTOM_BRACKET = (-1.5, -5.7)
SEAT = (-4.2, 3.2)  # top of the seat tube
HEAD_TOP = (5.0, 3.5)  # where the top tube meets the head tube
HEAD_BOTTOM = (5.8, 1.1)  # where the down tube meets the head tube
STEM_TOP = (4.3, 6.4)
BAR = [(4.3, 6.4), (7.6, 6.5), (8.8, 5.3), (8.4, 3.6)]  # a drop bar, hooking down
SADDLE = [(-7.0, 6.4), (-3.2, 6.4)]
SEAT_POST_TOP = (-4.8, 6.4)
TUBE_W = 1.6
BAR_W = 1.6
SADDLE_W = 1.8
DROPOUT = 4.0  # length of the solid wedge where the stays meet the rear hub
CLOSE_ISLANDS = 0.8  # rounds standing tips inside the wheels and frame past half the island minimum
CLOSE_WALLS = 0.6  # rounds the tips under the saddle and bar without filling the gap above the top tube


def _wheel(centre):
    return dot(*centre, 2 * WHEEL_R).difference(dot(*centre, 2 * (WHEEL_R - RIM_W)))


def _toward(a, b, length):
    du, dv = b[0] - a[0], b[1] - a[1]
    n = (du**2 + dv**2) ** 0.5
    return (a[0] + du * length / n, a[1] + dv * length / n)


def _close(geom, r):
    return geom.buffer(r, 16).buffer(-r, 16)


def draw():
    tubes = [
        [BOTTOM_BRACKET, SEAT],
        [SEAT, HEAD_TOP],
        [BOTTOM_BRACKET, HEAD_BOTTOM],
        [HEAD_BOTTOM, HEAD_TOP, STEM_TOP],
        [HEAD_BOTTOM, FRONT],
        [BOTTOM_BRACKET, REAR],
        [SEAT, REAR],
        [SEAT, SEAT_POST_TOP],
    ]
    dropout = Polygon([REAR, _toward(REAR, BOTTOM_BRACKET, DROPOUT), _toward(REAR, SEAT, DROPOUT)])
    core = _close(union(_wheel(REAR), _wheel(FRONT), dropout, *(stroke(t, TUBE_W) for t in tubes)), CLOSE_ISLANDS)
    bike = _close(union(core, stroke(BAR, BAR_W), stroke(SADDLE, SADDLE_W)), CLOSE_WALLS)
    return union(bike, dot(*REAR, HUB_D), dot(*FRONT, HUB_D))


motif = Motif(name="bicycle", issue=6, draw=draw)
