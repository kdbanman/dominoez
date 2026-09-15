"""A gymnast holding a straddle handstand, as a solid pictogram silhouette:
a short floor line, two straight arms planted a little wider than the
shoulders, the head hanging between them under a broad chest, a torso that
narrows to the waist and swells again at the hips, and two straight legs
opening in a wide V overhead, thick at the thigh and slimmer at the calf.

Every limb is the convex hull of a fat circle at its root and a thinner
one at its tip, so the body is made of tapered capsules that a closing
buffer blends into one outline."""

from shapely.geometry import Point

from ..geometry import stroke, union
from ..motif import Motif

# Joints are (u, v, radius); the figure is symmetric about u=0 and the right half is mirrored.
FLOOR = [(-10.2, -12.4), (10.2, -12.4)]
FLOOR_W = 1.6
HAND = (7.6, -10.9, 1.3)  # a round cap resting on the floor; wider than the shoulders so the pocket beside the head stays open
SHOULDER = (3.8, -3.0, 1.7)  # the arm tapers from here to the hand; the chest is the hull of the shoulders and waist
WAIST = (1.95, 3.3, 1.3)
HIP = (2.55, 5.6, 1.7)  # the leg tapers from here to the foot; the pelvis is the hull of the waist and hips
FOOT = (9.0, 11.2, 1.3)  # a round cap
HEAD = (0.0, -6.2, 1.7)  # tucked into the chest underside with no neck, as in a pictogram
ROUND = 0.5  # blunts the cut tips where a capsule ends in a point
CLOSE = 0.8  # fills the creases where limbs, head and floor meet


def _disc(u, v, r):
    return Point(u, v).buffer(r, 32)


def _capsule(*joints):
    """Convex hull of the discs at the joints: a limb that tapers from a fat root to a thin tip."""
    return union(*(_disc(*j) for j in joints)).convex_hull


def _mirror(joint):
    u, v, r = joint
    return (-u, v, r)


def _both(joint):
    return [joint, _mirror(joint)]


def draw():
    torso = union(_capsule(*_both(SHOULDER), *_both(WAIST)), _capsule(*_both(WAIST), *_both(HIP)))
    limbs = [_capsule(SHOULDER, HAND), _capsule(_mirror(SHOULDER), _mirror(HAND)), _capsule(HIP, FOOT), _capsule(_mirror(HIP), _mirror(FOOT))]
    gymnast = union(torso, _disc(*HEAD), stroke(FLOOR, FLOOR_W), *limbs)
    return gymnast.buffer(-ROUND, 16).buffer(ROUND, 16).buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="gymnast", issue=43, draw=draw)
