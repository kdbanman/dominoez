"""An ice pop: one wide slab with a fully rounded top and softly rounded
bottom corners, a single thin standing stripe across it where the two
flavours meet, on one fat stick."""

from shapely import affinity
from shapely.geometry import box

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

SLAB_W = 18.0
SLAB_TOP, SLAB_BOTTOM = 17.0, -4.0  # v of the slab's crown and its base
FOOT_ROUND = 2.5  # rounds the slab's bottom corners
STRIPE_V = 3.5  # v of the standing stripe across the slab, well below the crown so the top does not read as a cap
STRIPE_W = 1.3
STICK_W = 5.0
STICK_BOTTOM = -12.5
ROUND = 0.6


def draw():
    crown_r = SLAB_W / 2
    body = box(-SLAB_W / 2, SLAB_BOTTOM + FOOT_ROUND, SLAB_W / 2, SLAB_TOP - crown_r)
    foot_h = 2 * FOOT_ROUND + 0.1
    foot = affinity.translate(rounded_rect(SLAB_W, foot_h, FOOT_ROUND), 0, SLAB_BOTTOM + foot_h / 2)
    slab = union(body, foot, dot(0, SLAB_TOP - crown_r, 2 * crown_r))
    slab = slab.difference(stroke([(-SLAB_W, STRIPE_V), (SLAB_W, STRIPE_V)], STRIPE_W, cap="flat"))
    stick = stroke([(0, SLAB_BOTTOM + 1), (0, STICK_BOTTOM)], STICK_W)
    return union(slab, stick).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="popsicle", issue=120, draw=draw)
