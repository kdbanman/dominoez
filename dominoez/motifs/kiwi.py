"""A cute kiwi bird, side view, facing right, in its probing stance: a fat
body tilted nose-down, a round head held low, and a long thin beak angled
down toward the ground. Two stubby legs with forward-pointing feet; the eye
and a wing line are left standing."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

BODY_W, BODY_H = 17.0, 12.0  # ellipse axes
BODY_C = (-2.0, 1.0)
BODY_TILT = -15.0  # degrees; the front end drops
HEAD_R = 4.2
HEAD_C = (5.5, 2.0)
BEAK = [(8.0, 0.5), (12.5, -8.0)]
BEAK_W = 1.7
LEGS = [[(1.5, -4.0), (2.0, -9.5), (5.0, -9.5)], [(-5.5, -4.0), (-5.5, -9.5), (-3.0, -9.5)]]  # the feet stay past twice CLOSE apart
LEG_W = 1.8
EYE = (6.8, 3.0, 2.0)  # standing (u, v, diameter)
WING = [(-7.0, 1.5), (-3.5, 3.0), (0.0, 1.8)]  # standing
WING_W = 1.5
CLOSE = 1.0  # fills the creases where the head and legs meet the body


def draw():
    body = affinity.scale(Point(*BODY_C).buffer(1.0, 64), BODY_W / 2, BODY_H / 2, origin=BODY_C)
    body = affinity.rotate(body, BODY_TILT, origin=BODY_C)
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    kiwi = union(body, head, stroke(BEAK, BEAK_W), *(stroke(leg, LEG_W) for leg in LEGS))
    kiwi = kiwi.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return kiwi.difference(union(dot(*EYE), stroke(WING, WING_W)))


motif = Motif(name="kiwi", issue=27, draw=draw)
