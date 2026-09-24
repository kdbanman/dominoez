"""A cupcake: a fluted paper case, wider at the top, with standing flute
lines, a swirl of frosting in three plump tiers above a thin standing gap,
and a cherry with a short stem sitting as a bump on the top tier."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..geometry import dot, stroke, union
from ..motif import Motif

CASE_TOP, CASE_BOTTOM = -3.5, -12.0  # v of the case's rim and foot
CASE_W_TOP, CASE_W_BOTTOM = 20.0, 14.0
CASE_ROUND = 1.4  # rounds the case's corners
FLUTES = [-4.0, 0.0, 4.0]  # u of each standing flute line
FLUTE_W = 1.3
FLUTE_TOP = -5.0  # flutes run from below the foot up to here
GAP = 1.2  # standing line between case and frosting
TIERS = [
    [(-6.8, 0.0, 7.5), (0.0, 0.5, 8.0), (6.8, 0.0, 7.5)],  # bottom tier, widest
    [(-3.4, 4.6, 6.4), (3.4, 4.6, 6.4)],
    [(0.0, 8.2, 5.5)],  # top
]  # cut lumps (u, v, diameter)
CLOSE = 1.6  # knits the lumps into one swirl
CHERRY = (0.0, 11.2, 4.4)  # cut (u, v, diameter), sits as a bump on the top tier
STEM = [(0.0, 12.0), (1.8, 14.2)]
STEM_W = 1.6
ROUND = 0.6
STEM_CLOSE = 0.8  # fills the crease where the stem leaves the cherry
SCALE = 0.88  # laid out big, then shrunk so the top stays inside the box


def draw():
    case = Polygon([
        (-CASE_W_TOP / 2, CASE_TOP),
        (CASE_W_TOP / 2, CASE_TOP),
        (CASE_W_BOTTOM / 2, CASE_BOTTOM),
        (-CASE_W_BOTTOM / 2, CASE_BOTTOM),
    ]).buffer(-CASE_ROUND, 16).buffer(CASE_ROUND, 16)
    flutes = union(*(stroke([(u, CASE_BOTTOM - 1), (u, FLUTE_TOP)], FLUTE_W, cap="flat") for u in FLUTES))
    case = case.difference(flutes)
    frosting = union(*(dot(*lump) for tier in TIERS for lump in tier)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    frosting = frosting.difference(box(-20, -20, 20, CASE_TOP + GAP))
    cherry = union(dot(*CHERRY), stroke(STEM, STEM_W)).buffer(STEM_CLOSE, 16).buffer(-STEM_CLOSE, 16)
    frosting = union(frosting, cherry).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(union(case, frosting), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="cupcake", issue=119, draw=draw)
