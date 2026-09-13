"""A gymnast holding a straddle handstand on the floor: a floor line, two
straight arms planted from wide shoulders with the head hanging between
them, a fat vertical torso, and two straight legs opening in a V overhead.

A cartwheel (the same figure tipped 40 degrees onto one hand) was tried
and read as a figure falling over, so the handstand stayed."""

from ..geometry import dot, stroke, union
from ..motif import Motif

FLOOR = [(-7.5, -12.7), (7.5, -12.7)]  # a wall clear of the hands so the arm gaps stay open, not islands
FLOOR_W = 1.6
SHOULDERS = [(-3.6, -2.5), (3.6, -2.5)]
SHOULDER_W = 2.4
ARM = [(3.6, -2.5), (5.4, -9.5)]  # shoulder to hand; the left arm is mirrored
ARM_W = 2.4
HEAD = (0.0, -5.6, 3.8)  # (u, v, diameter), hanging from the shoulders with a wall past the minimum to each arm
TORSO = [(0.0, -2.5), (0.0, 4.0)]
TORSO_W = 3.4
LEG = [(0.0, 3.5), (4.2, 10.0)]  # hip to foot; the left leg is mirrored
LEG_W = 2.8
CLOSE = 0.5  # rounds the standing creases at the crotch, neck and hands without bridging the head gaps


def _mirror(points):
    return [(-u, v) for u, v in points]


def draw():
    gymnast = union(
        stroke(FLOOR, FLOOR_W),
        stroke(TORSO, TORSO_W),
        stroke(SHOULDERS, SHOULDER_W),
        stroke(ARM, ARM_W),
        stroke(_mirror(ARM), ARM_W),
        stroke(LEG, LEG_W),
        stroke(_mirror(LEG), LEG_W),
        dot(*HEAD),
    )
    return gymnast.buffer(CLOSE, 16).buffer(-CLOSE, 16)


motif = Motif(name="gymnast", issue=43, draw=draw)
