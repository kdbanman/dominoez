"""A trumpet side on, bell to the right, tilted up fifteen degrees: a
mouthpiece on the left, a fat lead pipe, three valve pistons standing on
it, a tuning loop hanging under it, and a wide bell that curves out to
its mouth."""

from shapely import affinity
from shapely.geometry import Polygon

from ..geometry import rounded_rect, stroke, union
from ..motif import Motif

PIPE = [(-10.5, 0.0), (5.0, 0.0)]  # the lead pipe from mouthpiece to bell
PIPE_W = 3.0
MOUTHPIECE = (2.8, 4.6, 1.0, (-10.8, 0.0))  # width, height, corner radius, centre
VALVES_U = [-4.4, -0.4, 3.6]  # centre of each piston along the pipe; the gaps between them are past the wall minimum
VALVE_W, VALVE_H, VALVE_V = 2.6, 6.6, 3.3  # each piston stands up from the pipe
VALVE_ROUND = 1.0
LOOP_W, LOOP_H, LOOP_C = 13.4, 6.4, (-0.8, -3.4)  # tuning loop hanging under the pipe: a solid block whose top hides in the pipe
LOOP_ROUND = 1.3
WINDOW_W, WINDOW_H, WINDOW_C = 8.4, 2.8, (-0.8, -3.0)  # standing window inside the loop, subtracted last; its corners are rounded so it survives the island check
WINDOW_ROUND = 1.0
# The bell, clockwise from its root on the pipe: the flare curves out to a bulged mouth and back
BELL = [(4.5, 1.7), (7.5, 2.6), (10.0, 4.4), (11.6, 6.6), (12.4, 7.6), (13.0, 0.0), (12.4, -7.6), (11.6, -6.6), (10.0, -4.4), (7.5, -2.6), (4.5, -1.7)]
TILT = 15.0  # degrees counter-clockwise
ROUND = 0.5  # blunts the bell's corners
SCALE = 0.92  # laid out big, then shrunk to fit the box once tilted


def draw():
    pipe = stroke(PIPE, PIPE_W)
    mouth = affinity.translate(rounded_rect(MOUTHPIECE[0], MOUTHPIECE[1], MOUTHPIECE[2]), *MOUTHPIECE[3])
    valves = union(*(affinity.translate(rounded_rect(VALVE_W, VALVE_H, VALVE_ROUND), u, VALVE_V) for u in VALVES_U))
    loop = affinity.translate(rounded_rect(LOOP_W, LOOP_H, LOOP_ROUND), *LOOP_C)
    bell = Polygon(BELL)
    trumpet = union(pipe, mouth, valves, loop, bell).buffer(-ROUND, 16).buffer(ROUND, 16)
    window = affinity.translate(rounded_rect(WINDOW_W, WINDOW_H, WINDOW_ROUND), *WINDOW_C)
    trumpet = affinity.scale(trumpet.difference(window), SCALE, SCALE, origin=(0, 0))
    return affinity.rotate(trumpet, TILT, origin=(0, 0))


motif = Motif(name="trumpet", issue=148, draw=draw)
