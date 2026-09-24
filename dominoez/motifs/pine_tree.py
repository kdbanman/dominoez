"""A pine tree: three fat overlapping wedges stacked on a stub trunk, each
tier wider than the one above, the bottom tier nearly as wide as the box.
One silhouette with blunted points."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..geometry import union
from ..motif import Motif

# (apex v, base v, base half-width) for each tier, top first; each base overlaps the tier below
TIERS = [(13.5, 4.5, 7.0), (9.0, -2.5, 10.2), (3.0, -9.5, 13.0)]
TRUNK_W, TRUNK_BOTTOM = 5.4, -12.8  # stub trunk under the bottom tier
ROUND = 0.9  # blunts the apex and the tier corners
CLOSE = 0.8  # smooths where a tier's base meets the tier below
SCALE = 0.94  # laid out big, then shrunk so the top stays inside the box


def draw():
    tiers = [Polygon([(0, apex), (half, base), (-half, base)]) for apex, base, half in TIERS]
    trunk = box(-TRUNK_W / 2, TRUNK_BOTTOM, TRUNK_W / 2, TIERS[-1][1] + 1.0)
    tree = union(*tiers, trunk).buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(tree, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="pine_tree", issue=122, draw=draw)
