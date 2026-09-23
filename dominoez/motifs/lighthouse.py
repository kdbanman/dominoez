"""A lighthouse on a rock: a tapered tower with two standing bands across
it, a wider gallery near the top, a lantern room with a domed cap, and two
fat wedges of light fanning up and out to either side. The tower stands
on a low rounded rock that sits in a wavy water line. Laid out big, then
scaled to fit."""

import math

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

TOWER = [(-4.8, -6.0), (4.8, -6.0), (3.0, 10.0), (-3.0, 10.0)]  # foot to top, tapering
BANDS = [(-1.5, 1.5), (4.5, 1.5)]  # standing stripes across the tower: (v, height)
GALLERY_C, GALLERY_W, GALLERY_H = (0.0, 10.4), 7.8, 2.2  # the walkway platform
LANTERN_C, LANTERN_W, LANTERN_H = (0.0, 13.2), 5.4, 3.6  # the glass room
DOME = (0.0, 14.6, 5.4)  # (u, v, diameter) cap on the lantern
BEAM_NEAR, BEAM_FAR = 3.0, 7.0  # wedge width at the lantern end and the far end
BEAM_LEN = 9.0
BEAM_GAP = 2.2  # standing gap between the lantern and each beam
BEAM_LIFT = 0.4  # beams leave the lantern a little above its middle
BEAM_TILT = 12.0  # degrees the beams rise from horizontal
ROCK_C, ROCK_W, ROCK_H = (0.0, -7.5), 17.0, 5.0  # rounded mound under the tower
WATER_SPAN = (-13.0, 13.0)
WAVE_LEN, WAVE_AMP = 8.67, 0.6
WAVE_V = -8.2  # runs through the lower half of the rock
WAVE_W = 2.0
ROUND = 0.55
SCALE = 0.9


def _beam(sign):
    u0 = sign * (LANTERN_W / 2 + BEAM_GAP)
    v0 = LANTERN_C[1] + BEAM_LIFT
    wedge = Polygon([(u0, v0 - BEAM_NEAR / 2), (u0 + sign * BEAM_LEN, v0 - BEAM_FAR / 2), (u0 + sign * BEAM_LEN, v0 + BEAM_FAR / 2), (u0, v0 + BEAM_NEAR / 2)])
    return affinity.rotate(wedge, sign * BEAM_TILT, origin=(u0, v0))


def draw():
    tower = Polygon(TOWER)
    gallery = affinity.translate(rounded_rect(GALLERY_W, GALLERY_H, 0.8), *GALLERY_C)
    lantern = affinity.translate(rounded_rect(LANTERN_W, LANTERN_H, 0.6), *LANTERN_C)
    dome = dot(*DOME).intersection(Polygon([(-10, DOME[1]), (10, DOME[1]), (10, 30), (-10, 30)]))
    rock = affinity.scale(dot(*ROCK_C, 2.0), ROCK_W / 2, ROCK_H / 2, origin=ROCK_C)
    u0, u1 = WATER_SPAN
    n = 64
    pts = [(u, WAVE_V + WAVE_AMP * math.sin(2 * math.pi * (u - u0) / WAVE_LEN)) for u in (u0 + (u1 - u0) * i / n for i in range(n + 1))]
    water = stroke(pts, WAVE_W)
    house = union(tower, gallery, lantern, dome, rock, water)
    house = house.buffer(-ROUND, 16).buffer(ROUND, 16)
    bands = union(*(affinity.translate(rounded_rect(12.0, h, 0.0), 0.0, v) for v, h in BANDS))
    house = house.difference(bands)
    beams = union(_beam(-1), _beam(1)).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(union(house, beams), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="lighthouse", issue=98, draw=draw)
