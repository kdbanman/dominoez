"""A cordless drill side-on, pointing right and tilted up a little: a
long rounded body with a blunt tapered chuck at the front, a pistol grip
slanting down from the back, a wide battery pack on the foot of the grip
and a trigger stub under the body."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, union
from ..motif import Motif

BODY = (16.0, 7.6, 2.2)  # motor housing: width, height, corner radius
BODY_C = (0.0, 5.0)
CHUCK = [(7.0, 7.8), (10.6, 7.2), (13.0, 6.3), (13.0, 3.7), (10.6, 2.8), (7.0, 2.2)]  # blunt taper at the nose
GRIP = [(-7.0, 2.5), (-1.2, 2.5), (-2.8, -7.0), (-8.6, -7.0)]  # slants back as it goes down
BATTERY = (11.0, 4.4, 1.2)  # wider pack across the foot of the grip, reaching forward under the trigger
BATTERY_C = (-4.2, -8.6)
TRIGGER = (2.6, 3.6, 0.8)
TRIGGER_C = (1.2, 0.2)
TILT = 12.0  # degrees, nose up
SCALE = 1.05  # laid out a touch small, then grown to fill the width
CLOSE = 0.8  # blends the grip and chuck into the body
ROUND = 0.6


def draw():
    body = affinity.translate(rounded_rect(*BODY), *BODY_C)
    battery = affinity.translate(rounded_rect(*BATTERY), *BATTERY_C)
    trigger = affinity.translate(rounded_rect(*TRIGGER), *TRIGGER_C)
    drill = union(body, Polygon(CHUCK), Polygon(GRIP), battery, trigger)
    drill = drill.buffer(CLOSE, 16).buffer(-CLOSE, 16).buffer(-ROUND, 16).buffer(ROUND, 16)
    return affinity.scale(affinity.rotate(drill, TILT, origin=(0, 0)), SCALE, SCALE, origin=(0, 0))


motif = Motif(name="drill", issue=142, draw=draw)
