"""A paint brush tilted diagonally, bristles up and to the right: a thin
handle with a rounded butt, a short wider ferrule collar, and a splayed
block of bristles that flares out past everything else and ends in a soft
rounded edge. Thin standing lines part the three pieces so the ferrule
reads as a metal band, and two standing notches run in from the tip to
suggest the hairs."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..geometry import stroke, union
from ..motif import Motif

# Drawn upright along v, bristles at the top, then tilted.
HANDLE_W, HANDLE_L = 3.0, 13.0
FERRULE_W, FERRULE_L = 5.0, 3.0
BRISTLE_W, BRISTLE_L = 5.4, 8.0  # width at the ferrule, length to the tip
BRISTLE_TIP_W = 9.0  # width of the tip before its corners are rounded; the widest part of the brush
TIP_BULGE = 1.0  # how far the middle of the tip edge bows out past its corners
GAP = 1.2  # standing line between handle, ferrule and bristles, past the wall minimum
HAIRS = [-2.6, 0.0, 2.6]  # u of each standing notch running in from the tip
HAIR_LEN, HAIR_W = 1.8, 1.2  # notch length from the tip edge, width past the wall minimum
TILT = -45.0  # degrees; negative leans the bristles to the right
ROUND = 1.0  # rounds the handle butt and the bristle tip
BLUNT = 0.5  # rounds the cut tips between the hair notches


def _open(geom, r):
    return geom.buffer(-r, 16).buffer(r, 16)


def draw():
    v0 = -(HANDLE_L + GAP + FERRULE_L + GAP + BRISTLE_L) / 2  # handle butt
    handle = box(-HANDLE_W / 2, v0, HANDLE_W / 2, v0 + HANDLE_L)
    v1 = v0 + HANDLE_L + GAP
    ferrule = box(-FERRULE_W / 2, v1, FERRULE_W / 2, v1 + FERRULE_L)
    v2 = v1 + FERRULE_L + GAP
    v3 = v2 + BRISTLE_L
    outline = [(-BRISTLE_W / 2, v2), (BRISTLE_W / 2, v2), (BRISTLE_TIP_W / 2, v3), (0.0, v3 + TIP_BULGE), (-BRISTLE_TIP_W / 2, v3)]
    bristles = _open(Polygon(outline), ROUND)
    hairs = union(*(stroke([(u, v3 + TIP_BULGE + HAIR_W), (u, v3 + TIP_BULGE - HAIR_LEN)], HAIR_W) for u in HAIRS))
    bristles = _open(bristles.difference(hairs), BLUNT)
    brush = union(_open(handle, ROUND), ferrule, bristles)
    return affinity.rotate(brush, TILT, origin=(0, 0))


motif = Motif(name="paint_brush", issue=40, draw=draw)
