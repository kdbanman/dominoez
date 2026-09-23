"""An astronaut pictogram, front on: a big round helmet, a standing collar
ring parting it from a chunky rounded body, two fat arms held out and
down, two short legs on wide boots, and a backpack that shows as square
shoulders poking out behind the helmet."""

from shapely import affinity

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

HELMET = (0.0, 8.0, 11.5)  # (u, v, diameter)
COLLAR = 1.3  # standing ring between helmet and body, past the wall minimum
BODY_C, BODY_W, BODY_H = (0.0, -1.5), 11.0, 10.0  # rounded chest and belly
PACK_C, PACK_W, PACK_H = (0.0, 2.5), 15.0, 6.0  # backpack, wider than the body, showing at the shoulders
ARMS = [[(-4.0, 1.5), (-8.5, -5.5)], [(4.0, 1.5), (8.5, -5.5)]]  # shoulder to glove
ARM_W = 3.6
GLOVE_D = 4.0
LEGS = [[(-2.6, -5.0), (-3.2, -10.5)], [(2.6, -5.0), (3.2, -10.5)]]
LEG_W = 3.6
BOOT_W, BOOT_H = 5.0, 2.6
BOOT_V = -11.5
ROUND = 0.55
CLOSE = 0.8  # blends limbs and pack into the body


def draw():
    body = affinity.translate(rounded_rect(BODY_W, BODY_H, 3.5), *BODY_C)
    pack = affinity.translate(rounded_rect(PACK_W, PACK_H, 1.5), *PACK_C)
    arms = union(*(stroke(a, ARM_W) for a in ARMS), *(dot(*a[1], GLOVE_D) for a in ARMS))
    legs = union(*(stroke(l, LEG_W) for l in LEGS))
    boots = union(*(affinity.translate(rounded_rect(BOOT_W, BOOT_H, 1.0), l[1][0] - (0.5 if l[1][0] < 0 else -0.5), BOOT_V) for l in LEGS))
    suit = union(body, pack, arms, legs, boots)
    suit = suit.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    helmet = dot(*HELMET)
    suit = suit.difference(helmet.buffer(COLLAR, 16))
    return union(suit, helmet)


motif = Motif(name="astronaut", issue=107, draw=draw)
