"""A snowflake: six fat arms from a round hub, one straight up, each arm
carrying one pair of short branches angled outward part way along. No
filigree."""

import math

from shapely import affinity
from shapely.geometry import Point

from ..geometry import stroke, union
from ..motif import Motif

ARMS = 6
ARM_LEN = 12.4  # from the centre to each arm's tip
ARM_W = 2.8
HUB_D = 5.0  # round hub at the centre
BRANCH_AT = 7.6  # distance along the arm where the branch pair sprouts
BRANCH_LEN = 4.0
BRANCH_ANGLE = 50.0  # degrees off the arm, either side
BRANCH_W = 2.5
TIP_D = 3.4  # blob at each arm's tip
CLOSE = 0.8  # rounds the creases where the branches leave the arm, so the standing wedge there stays printable
ROUND = 0.5  # blunts the ends
SCALE = 0.97  # laid out big, then shrunk so the top arm stays inside the box


def _arm(i):
    a = math.radians(BRANCH_ANGLE)
    arm = stroke([(0.0, 0.0), (ARM_LEN, 0.0)], ARM_W)
    tip = Point(ARM_LEN, 0.0).buffer(TIP_D / 2, 32)
    branches = union(*(stroke([(BRANCH_AT, 0.0), (BRANCH_AT + BRANCH_LEN * math.cos(a), s * BRANCH_LEN * math.sin(a))], BRANCH_W) for s in (1, -1)))
    return affinity.rotate(union(arm, tip, branches), 90.0 + 360.0 * i / ARMS, origin=(0, 0))


def draw():
    flake = union(Point(0, 0).buffer(HUB_D / 2, 48), *(_arm(i) for i in range(ARMS)))
    flake = flake.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(flake, SCALE, SCALE, origin=(0, 0))


motif = Motif(name="snowflake", issue=130, draw=draw)
