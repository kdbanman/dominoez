"""A unicorn head in side profile, facing right: a round head with a
blunt muzzle, a thick neck dropping away to the lower left, a long horn
rising from the brow, a pricked ear, and a wavy mane of lobes down the
back of the neck parted from it by a standing line. The eye is left
standing."""

from shapely.geometry import Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_C = (2.0, 3.0)
HEAD_R = 5.2
MUZZLE = [(3.0, 2.0), (8.5, 0.0)]  # centreline from the head to the nose
MUZZLE_W = 6.0
NECK = [(-0.5, 1.0), (-3.5, -7.5)]  # centreline, head end first
NECK_W = 8.0
HORN = [(0.0, 7.5), (3.2, 7.5), (2.6, 16.0)]  # base left, base right, tip
EAR = [(-3.8, 5.8), (-0.8, 7.2), (-2.4, 11.6)]  # base left, base right, tip
MANE = [(-4.0, 5.4, 5.2), (-6.4, 1.6, 5.4), (-8.4, -2.4, 5.4), (-9.8, -6.6, 5.0)]  # (u, v, diameter) lobes down the back
MANE_LINE = [(-2.6, 4.0), (-4.8, 0.2), (-6.6, -3.6), (-7.8, -7.4), (-8.2, -10.0)]  # standing line between the mane and the neck
MANE_LINE_W = 1.2
EYE = (3.8, 4.4, 2.2)  # standing (u, v, diameter)
NOSTRIL = (8.2, 0.6, 1.8)  # standing (u, v, diameter)
BLUNT = 0.7  # rounds the horn and ear tips past half the channel minimum
CLOSE = 0.8  # fills the creases where the muzzle, neck, ear and horn meet the head

def draw():
    head = dot(*HEAD_C, 2 * HEAD_R)
    horn = Polygon(HORN).buffer(-BLUNT, 8).buffer(BLUNT, 8)
    ear = Polygon(EAR).buffer(-BLUNT, 8).buffer(BLUNT, 8)
    mane = union(*(dot(u, v, d) for u, v, d in MANE))
    body = union(head, stroke(MUZZLE, MUZZLE_W), stroke(NECK, NECK_W), horn, ear, mane)
    body = body.buffer(CLOSE, 16).buffer(-CLOSE, 16)
    standing = union(dot(*EYE), dot(*NOSTRIL), stroke(MANE_LINE, MANE_LINE_W))
    return body.difference(standing)


motif = Motif(name="unicorn", issue=35, draw=draw)
