"""The Canadian flag maple leaf, traced from the flag's SVG path
(Wikimedia Commons, Flag_of_Canada.svg) and scaled to 26 mm tall: a
narrow top spike, double-pointed upper lobes, wide side lobes with their
outer tips pointing out, two down-pointing tips flanking the stem. The
flag's stem would be 1.2 mm wide at this size, so a fatter one stands
in; the shallow notch under each side tip is deepened a little so the
closing does not swallow it."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..geometry import union
from ..motif import Motif

# The right half of the flag leaf's outline in mm, top tip to the stem's shoulder, with the notch under the side tip deepened. Mirrored for the left half.
HALF = [
    (0.0, 13.0),  # top spike
    (2.14, 8.79), (2.73, 8.62),  # notch
    (4.84, 9.84),  # upper lobe, first point
    (3.52, 3.05), (4.24, 2.68),  # deep notch
    (6.97, 5.61),  # upper lobe, second point
    (7.65, 4.02), (8.12, 3.77),  # notch
    (11.61, 4.52),  # side lobe, upper tip
    (10.0, 0.9), (10.2, 0.3),  # notch, deepened from the flag's (10.4, 0.8) and (10.6, 0.3)
    (12.0, -0.32),  # side lobe, outer tip
    (5.93, -5.24), (5.8, -5.71),  # deep notch
    (6.55, -7.77),  # down-pointing tip
    (1.01, -6.8),  # the stem's shoulder
]
STEM_W, STEM_BOTTOM = 2.6, -13.0  # stem straight down from the skirt
CLOSE = 0.75  # rounds the bottom of every notch to 1.5 mm across, so each stays a printable standing gap
ROUND = 0.7  # blunts the tips
SCALE = 1.0


def draw():
    left = [(-u, v) for u, v in reversed(HALF[1:])]
    leaf = union(Polygon(HALF + left), box(-STEM_W / 2, STEM_BOTTOM, STEM_W / 2, HALF[-1][1] + 1.0))
    leaf = leaf.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(leaf, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="maple_leaf", issue=125, draw=draw)
