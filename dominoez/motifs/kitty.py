"""A cat sitting in side profile, facing right: a round head with two pointed
ears on a plump body that sits back on a big round haunch, one straight
front leg with a paw, and a tail that sweeps out behind and curls up to a
free tip. The eye and the crease between the front leg and the chest are
left standing."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_R = 4.4
HEAD_C = (5.0, 5.0)
EARS = [[(1.4, 7.4), (1.6, 12.0), (5.0, 9.3)], [(5.8, 9.3), (8.8, 11.8), (8.8, 7.4)]]  # base, tip, base
CHEST_W, CHEST_H = 10.0, 15.0  # ellipse axes, tilted so the chest leans forward under the head
CHEST_C = (2.0, -3.0)
CHEST_TILT = -12.0  # degrees
HAUNCH_R = 6.2
HAUNCH_C = (-3.5, -5.2)
LEG = [(5.5, -3.0), (5.5, -9.3)]  # the front leg, straight down
LEG_W = 3.4
PAW = (6.5, -9.6, 3.6)  # (u, v, diameter) the front paw, poking forward
BACK_PAW = (1.0, -9.8, 3.6)  # the hind paw under the haunch
TAIL = [(-7.5, -9.2), (-10.5, -9.4), (-12.5, -7.5), (-13.3, -4.5), (-12.8, -1.5), (-11.3, 0.8), (-9.5, 1.6)]  # from the rump, sweeping out and up to a free tip clear of the back
TAIL_W = 2.6
EYE = (6.6, 5.8, 1.9)  # standing (u, v, diameter)
LEG_LINE = [(3.5, -4.5), (3.5, -7.5)]  # standing crease between leg and chest
LEG_LINE_W = 1.6
ROUND = 0.7  # blunts the ear tips past half the channel minimum
CLOSE = 0.8  # fills the creases where head, haunch, paws and tail meet the body


def draw():
    head = Point(*HEAD_C).buffer(HEAD_R, 64)
    ears = [Polygon(e).buffer(-ROUND, 8).buffer(ROUND, 8) for e in EARS]
    chest = affinity.scale(Point(*CHEST_C).buffer(1.0, 64), CHEST_W / 2, CHEST_H / 2, origin=CHEST_C)
    chest = affinity.rotate(chest, CHEST_TILT, origin=CHEST_C)
    haunch = Point(*HAUNCH_C).buffer(HAUNCH_R, 64)
    cat = union(head, *ears, chest, haunch, stroke(LEG, LEG_W), dot(*PAW), dot(*BACK_PAW), stroke(TAIL, TAIL_W))
    cat = cat.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return cat.difference(union(dot(*EYE), stroke(LEG_LINE, LEG_LINE_W)))


motif = Motif(name="kitty", issue=47, draw=draw)
