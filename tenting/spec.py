"""Every dimension of the tenting cradle, in millimetres.

Plate coordinates are TOTEMX's own: the left half seen from above, pinky edge at -x,
thumb cluster at +x, top edge (controller and jacks) at +y, the bottom face at z = 0.
"""

# The outline of the TOTEMX bottom plate's underside, left half. Traced from the low-profile
# case's bottom plate (Case/Low Profile/totemx-low-profile-case.3mf in azhizhinov/TOTEMX,
# CERN-OHL-P), whose outline is the same as Case/20250215.TOTEMX.BOTTOMPLATE.00.stl.
# The 20250211 and 20250806 cases' bottom trays are 3 mm bigger all round the main body.
OUTLINE = [
    (12.86, -7.47), (4.34, -2.55), (4.34, 76.02), (-49.0, 76.02), (-49.0, 80.73), (-68.05, 80.73),
    (-68.05, 76.02), (-117.58, 76.02), (-117.58, 20.44), (-126.4, 18.88), (-123.1, 0.12),
    (-117.58, 1.09), (-117.58, -9.71), (-57.71, -9.71), (-57.71, -13.61), (-36.06, -13.61),
    (-18.42, -18.34), (0.33, -29.17),
]

TILT = 35.0        # tenting angle, about a front-to-back axis under the outermost pinky edge
SLOP = 0.5         # pocket clearance around the plate, each side
WALL = 2.0         # lip thickness
LIP = 5.0          # lip height above the plate's bottom face
FEET = 1.0         # the keyboard's own rubber feet stand the plate this far off the pocket floor
FLOOR = 0.6        # pocket floor above the desk at the pivot: three 0.2 mm layers
DECK = 3.0         # material under the pocket floor before the wedge, measured square to the floor

DESK_FOOT_D = 13.0      # pockets for stick-on rubber feet under the cradle
DESK_FOOT_DEPTH = 2.0
DESK_FOOT_MARGIN = 1.5  # solid around each pocket
DESK_FOOT_SKIN = 11.0   # how far in from the pivot edge the wedge is thick enough for a pocket

# The lip is cut down to the pocket floor where the plate's walls open for a connector or
# the power switch. Rectangles in plate coordinates (x0, y0, x1, y1), placed from the
# TOTEMX PCB (TOTEMX.kicad_pcb) and checked against the openings in the case's walls.
NOTCHES = {
    "xiao_usb": (-115.5, 60.0, -94.5, 120.0),    # XIAO's USB-C, top edge, pinky side
    "trrs_and_usb": (-12.1, 45.4, 40.0, 120.0),  # TRRS on the top edge and USB-C on the inner edge: one corner cut
    "power_switch": (-140.0, 22.0, -110.0, 34.0),  # slide switch on the pinky edge
}

BED = 290.0
