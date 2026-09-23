"""A hot air balloon drifting with a slight lean: a big teardrop envelope,
round at the top and narrowing to a small mouth, with two standing gore
seams curving down its sides, and below it a small basket hung on two
short ropes, with a standing gap between the mouth and the ropes."""

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

TOP_C, TOP_D = (0.0, 5.5), 20.5  # the round crown of the envelope
MOUTH_C, MOUTH_D = (0.0, -6.5), 5.5  # the small round mouth; the envelope is the hull of the two
GORES = [-0.5, 0.5]  # standing seams, as copies of the outline squeezed sideways by this factor
GORE_W = 1.4
GORE_CLIP = (-5.5, 13.0)  # v range the seams are kept in, so they stop short of the crown and the mouth
ROPES = [[(-2.2, -8.2), (-2.8, -11.5)], [(2.2, -8.2), (2.8, -11.5)]]
ROPE_W = 1.6
BASKET_C, BASKET_W, BASKET_H = (0.0, -13.2), 7.5, 3.8
GAP = 1.4  # standing gap between the mouth and the ropes
LEAN = -8.0  # degrees; the balloon drifts to the right
ROUND = 0.55
CLOSE = 0.8


def draw():
    envelope = union(Point(TOP_C).buffer(TOP_D / 2, 96), Point(MOUTH_C).buffer(MOUTH_D / 2, 48)).convex_hull
    clip = Polygon([(-20, GORE_CLIP[0]), (20, GORE_CLIP[0]), (20, GORE_CLIP[1]), (-20, GORE_CLIP[1])])
    seams = union(*(affinity.scale(envelope, f, 1.0, origin=(0, 0)).exterior for f in GORES)).buffer(GORE_W / 2).intersection(clip)
    envelope = envelope.difference(seams)
    ropes = union(*(stroke(rope, ROPE_W) for rope in ROPES))
    basket = affinity.translate(rounded_rect(BASKET_W, BASKET_H, 0.9), *BASKET_C)
    rig = union(ropes, basket).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    balloon = union(envelope.difference(rig.buffer(GAP, 16)), rig)
    balloon = balloon.buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.rotate(balloon, LEAN, origin=(0.0, 0.0))


motif = Motif(name="hot_air_balloon", issue=99, draw=draw)
