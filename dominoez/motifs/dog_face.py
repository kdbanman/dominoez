"""A dog's face, front on. A round head with floppy ears hanging past the
cheeks; eyes, a big nose and a smile left standing."""

from shapely import affinity
from shapely.geometry import Point

from ..geometry import dot, stroke, union
from ..motif import Motif

HEAD_R = 8.5
EAR = [(6.5, 5.5), (9.0, -6.5)]  # right ear, top to tip; the left is mirrored
EAR_W = 5.0
EYES = [(-3.3, 2.2), (3.3, 2.2)]
EYE_D = 2.6
NOSE_C = (0.0, -1.5)
NOSE_W, NOSE_H = 4.0, 3.0
MOUTH = [[(0.0, -2.5), (0.0, -6.2)], [(-3.5, -4.4), (-2.4, -5.6), (0.0, -6.2), (2.4, -5.6), (3.5, -4.4)]]
FEATURE_W = 1.8
ROUND = 0.8
CLOSE = 0.6  # fills the crease where each ear leaves the cheek


def draw():
    head = Point(0, 0).buffer(HEAD_R, 64)
    ears = [stroke(EAR, EAR_W), stroke([(-u, v) for u, v in EAR], EAR_W)]
    dog = union(head, *ears).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    nose = affinity.scale(Point(*NOSE_C).buffer(1.0, 32), NOSE_W / 2, NOSE_H / 2)
    features = union(
        *(dot(u, v, EYE_D) for u, v in EYES),
        nose,
        *(stroke(m, FEATURE_W) for m in MOUTH),
    ).buffer(-ROUND, 16).buffer(ROUND, 16)
    return dog.difference(features)


motif = Motif(name="dog_face", issue=11, draw=draw)
