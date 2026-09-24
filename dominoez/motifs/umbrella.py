"""An open umbrella: a solid domed canopy with a scalloped edge of four
scallops and a stub on top, and a fat shaft from the middle of the
canopy down to a hook curling to the left."""

import math

from shapely import affinity
from shapely.geometry import Point, box

from ..geometry import stroke, union
from ..motif import Motif

CANOPY_W, CANOPY_H = 26.0, 11.5  # the canopy is the top half of an ellipse this wide and twice this tall
CANOPY_V = 0.0  # v of the canopy's straight edge
SCALLOPS = [-9.75, -3.25, 3.25, 9.75]  # u of each scallop's centre along the edge
SCALLOP_R = 3.5
SCALLOP_V = -1.5  # the scallop discs sit this far below the edge so they bite shallow arcs
TIP = [(0.0, CANOPY_H - 1.0), (0.0, CANOPY_H + 2.0)]  # stub on the crown
TIP_W = 2.6
SHAFT = [(0.0, 1.0), (0.0, -12.0)]  # from inside the canopy's edge down to the hook
SHAFT_W = 2.6
HOOK_C, HOOK_R, HOOK_SWEEP = (-3.4, -12.0), 3.4, 200.0  # the hook is an arc below the shaft's end, curling up on the left
ROUND = 0.5  # blunts the scallop points and the hook's end
CLOSE = 0.8  # blends the tip into the canopy and the hook into the shaft


def _hook():
    steps = 20
    pts = [(HOOK_C[0] + HOOK_R * math.cos(math.radians(a)), HOOK_C[1] + HOOK_R * math.sin(math.radians(a))) for a in [-HOOK_SWEEP * i / steps for i in range(steps + 1)]]
    return stroke(pts, SHAFT_W)


def draw():
    dome = affinity.scale(Point(0, CANOPY_V).buffer(1.0, 96), CANOPY_W / 2, CANOPY_H, origin=(0, CANOPY_V))
    canopy = dome.intersection(box(-CANOPY_W, CANOPY_V, CANOPY_W, CANOPY_V + CANOPY_H + 1))
    canopy = canopy.difference(union(*(Point(u, SCALLOP_V).buffer(SCALLOP_R, 48) for u in SCALLOPS)))
    canopy = union(canopy, stroke(TIP, TIP_W)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    handle = union(stroke(SHAFT, SHAFT_W), _hook()).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    return union(canopy, handle).buffer(-ROUND, 16).buffer(ROUND, 16)


motif = Motif(name="umbrella", issue=131, draw=draw)
