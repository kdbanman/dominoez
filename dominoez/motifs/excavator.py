"""A toy excavator seen from the side, facing right, mid-dig: one long
rounded track, a small house with a cab and a standing window on top, and
a single bent arm of fat strokes rising steeply from the house to a
knuckle and dropping to a boxy bucket, a fat trapezoid whose lip faces
the machine and carries three square teeth, hanging forward past the
track's front."""

from shapely import affinity
from shapely.geometry import Polygon, box

from ..geometry import dot, rounded_rect, stroke, union
from ..motif import Motif

TRACK_W, TRACK_H, TRACK_C = 15.0, 5.0, (-2.5, -13.0)  # one rounded track pad and its centre
HOUSE_W, HOUSE_H, HOUSE_C = 8.0, 6.0, (-4.0, -7.0)  # turret on the track
CAB_W, CAB_H, CAB_C = 6.0, 7.5, (-1.5, -0.75)  # cab rises from the front of the house
WINDOW_W, WINDOW_H, WINDOW_C = 3.2, 3.0, (-1.3, 0.2)  # standing, a wall inside the cab
ARM = [(0.5, -5.0), (6.0, 6.5), (14.0, -2.0)]  # house, knuckle, wrist: one bent arm, the wrist inside the bucket's back
ARM_W = 3.8
BUCKET = [(7.5, -0.5), (15.0, -1.5), (13.0, -8.5), (8.0, -8.5)]  # boxy bucket, lip on the left facing the machine
TEETH_V = [-2.0, -4.8, -7.6]  # v of each square tooth's centre along the lip
TOOTH = (1.5, 1.6)  # (reach past the lip, width along the lip)
LIP_U = 8.1  # u the teeth are drawn back to, inside the bucket, so they join it
ROUND = 0.6  # blunts every tip
CLOSE = 0.7  # bridges the arm's joints and the wrist into the bucket without filling the crook; the teeth are added afterwards so they stay parted
SCALE = 0.92  # laid out big, then shrunk so the bucket stays inside the box


def _teeth():
    reach, width = TOOTH
    return union(*(box(LIP_U - reach - 1.0, v - width / 2, LIP_U, v + width / 2) for v in TEETH_V))


def draw():
    track = affinity.translate(rounded_rect(TRACK_W, TRACK_H, TRACK_H / 2), *TRACK_C)
    house = affinity.translate(rounded_rect(HOUSE_W, HOUSE_H, 1.2), *HOUSE_C)
    cab = affinity.translate(rounded_rect(CAB_W, CAB_H, 1.5), *CAB_C)
    arm = union(stroke(ARM, ARM_W), dot(*ARM[-1], ARM_W))
    machine = union(track, house, cab, arm, Polygon(BUCKET)).buffer(CLOSE, 16).buffer(-CLOSE, 16)
    machine = union(machine, _teeth()).buffer(-ROUND, 16).buffer(ROUND, 16)
    window = affinity.translate(rounded_rect(WINDOW_W, WINDOW_H, 0.9), *WINDOW_C)
    return affinity.scale(machine.difference(window), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="excavator", issue=101, draw=draw)
