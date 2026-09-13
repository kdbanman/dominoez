"""A cute unicorn head in side profile, facing right, as a bust: a round
skull with a soft muzzle, a thick neck cut flat at the base, a mane of plump
scallops down the back of the neck, a slender banded horn, and a small ear.
The eye, nostril and horn bands are left standing."""

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from ..geometry import dot, stroke, union
from ..motif import Motif

SKULL_C, SKULL_R = (0.0, 3.0), 5.8
MUZZLE = [(2.0, 2.0), (8.0, -2.5)]  # centreline from skull to nose
MUZZLE_W = 6.0
NECK = [(-4.5, 1.0), (2.5, -2.0), (1.5, -10.0), (-9.0, -10.0)]  # ends flat at the base
MANE = [(-5.5, 7.0, 6.0), (-8.0, 2.5, 6.6), (-10.0, -2.5, 6.2), (-10.5, -7.5, 5.8)]  # (u, v, diameter)
HORN_BASE, HORN_LEN, HORN_ANGLE = (0.0, 8.0), 8.0, 72.0  # degrees from horizontal
HORN_W, HORN_TIP = 3.2, 1.8
BANDS = 2
BAND_LEN = 4.4  # a little past the horn width, so the cut is clean
BAND_W = 1.25  # standing bands across the horn, past the wall minimum after SCALE
EAR_BASE, EAR_LEN, EAR_ANGLE = (-3.5, 7.0), 4.0, 108.0
EAR_W = 2.6
EYE = (2.6, 3.5, 3.2)  # standing (u, v, diameter)
NOSTRIL = (7.8, -2.0, 1.9)  # past the island minimum after SCALE
CLOSE = 1.3  # blends the parts into one silhouette
SCALE = 0.82  # the head is laid out big, then shrunk to fit the box
BASE_ROUND = 1.2  # rounds the corners of the flat base


def _taper(base, length, angle, w0, w1):
    """A rounded taper from a base of width w0 to a tip of width w1."""
    a = math.radians(angle)
    du, dv = math.cos(a), math.sin(a)
    nu, nv = -dv, du
    bu, bv = base
    tu, tv = bu + du * length, bv + dv * length
    body = Polygon([
        (bu + nu * w0 / 2, bv + nv * w0 / 2),
        (tu + nu * w1 / 2, tv + nv * w1 / 2),
        (tu - nu * w1 / 2, tv - nv * w1 / 2),
        (bu - nu * w0 / 2, bv - nv * w0 / 2),
    ])
    return union(body, dot(tu, tv, w1))


def _bands():
    a = math.radians(HORN_ANGLE)
    du, dv = math.cos(a), math.sin(a)
    bu, bv = HORN_BASE
    parts = []
    for i in range(BANDS):
        d = HORN_LEN * (i + 1.2) / (BANDS + 1.2)
        cu, cv = bu + du * d, bv + dv * d
        band = stroke([(cu - BAND_LEN / 2, cv), (cu + BAND_LEN / 2, cv)], BAND_W, cap="flat")
        parts.append(affinity.rotate(band, HORN_ANGLE + 85.0, origin=(cu, cv)))
    return union(*parts)


def draw():
    skull = Point(*SKULL_C).buffer(SKULL_R, 64)
    muzzle = stroke(MUZZLE, MUZZLE_W)
    neck = Polygon(NECK).buffer(-BASE_ROUND, 16).buffer(BASE_ROUND, 16)
    mane = union(*(dot(u, v, d) for u, v, d in MANE))
    horn = _taper(HORN_BASE, HORN_LEN, HORN_ANGLE, HORN_W, HORN_TIP)
    ear = _taper(EAR_BASE, EAR_LEN, EAR_ANGLE, EAR_W, 1.6)
    head = union(skull, muzzle, neck, mane, ear).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    unicorn = union(head, horn)
    standing = union(dot(*EYE), dot(*NOSTRIL), _bands())
    return affinity.scale(unicorn.difference(standing), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="unicorn", issue=35, draw=draw)
