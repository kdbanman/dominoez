"""Every dimension of the reel, in mm.

World axes: x along the axle, y across in the wheel's plane, z up. The axle centre is
the origin, the reel hanging unloaded.
"""

import math

# ---- wheel
FLANGE_R = 50.0          # 4" wheel
FLOOR_R = 35.0           # groove floor; 10 lb holds with 44.5 N x 35 mm = 1.56 N m
LOWER_FLANGE = 3.0       # flat flange on the bed
FLOOR_W = 6.0            # groove floor width
TOP_RIM = 2.0            # vertical rim above the 45 degree flank
SHELL = 3.0              # wall of the cup and the 45 degree flank, normal to the surface
WEB = 5.0                # disc between hub and drum, carrying the lock holes
HUB_R = 16.0
LOCK_N = 10              # lock positions, every 36 degrees
LOCK_R = 24.0            # pitch radius of the lock holes
ANCHOR_D = 2.5           # line anchor hole through the groove floor
WHEEL_W = LOWER_FLANGE + FLOOR_W + (FLANGE_R - FLOOR_R) + TOP_RIM

# ---- pins and their holes
PENCIL_HOLE = 8.4        # lock and hinge: takes a round pencil crayon (about 7.5) or the printed pin
PENCIL_PIN = 7.8
CROSS_HOLE = 6.6         # the shaft is only 11.4 thick, so the cross pin stays small
CROSS_PIN = 6.2
PIN_FLAT = 0.8           # flat on each pin's underside: it lies on the bed, only its first mm overhangs
PIN_TAB = (4.0, 16.0)    # head tab: length along the pin, width across
LOCK_PIN_L = 45.0
HINGE_PIN_L = 45.0
CROSS_PIN_L = 17.0       # snap catch just past the shaft

# ---- axle tube and crank
GAP = 1.0                # wheel face to cheek
CHEEK_T = 6.0
BEAR_HEAD = 24.0         # tube bearing in the head-side cheek
BEAR_SNAP = 20.0         # tube bearing in the snap-side cheek; passes through the wheel's hex
BEAR_CLEAR = 0.6         # on diameter
TUBE_HEAD_D = 30.0
TUBE_HEAD_T = 3.0
TUBE_HEX_AF = 21.0       # drives the wheel; corners 24.2 pass the head-side hole
WHEEL_HEX_AF = 21.3
BORE_HEX_AF = 12.0       # the crank's socket
CRANK_HEX_AF = 11.7
CRANK = 50.0             # crank radius
CRANK_ARM_T = 8.0
KNOB_L = 24.0

# ---- chassis
PIVOT_Z = 70.0           # hinge pin above the axle
PIVOT_DROP = 18.0        # hinge pin below the plywood
BRIDGE_R = 15.0          # the bridge's top is round about the hinge pin
BRIDGE_FLAT = 17.0       # its flat underside, spanning between the cheeks, this far below the pin
TONGUE_R = 10.0
SLOT_CLEAR = 0.8         # tongue slot, on width
SWING = 65.0             # the reel's swing on the hinge pin either side of vertical
FOOT_HALF = 40.0         # half-width of each cheek's foot
FOOT_Z = -26.0
FOOT_FLARE = 4.0         # 45 degree flare outside each foot
WINDOW = (150.0, 210.0)  # degrees on the lock circle; shows holes at 162 and 198 when 90 is under the pin
WINDOW_W = 11.0

# ---- hanger shaft and the shelf it hangs from
BOARD_T = 19.0           # 3/4" plywood as measured
BOARD_HOLE = 12.7        # 1/2"
SHAFT_AF = 11.4          # octagon across flats; corners 12.34 in the 12.7 hole
CROSS_ABOVE = CROSS_PIN / 2 + 0.3   # cross pin centre above the plywood: it rests on the board
SHAFT_TOP = 7.0          # shaft past the cross pin

# ---- derived
XI = WHEEL_W / 2 + GAP                       # cheek inner face
XO = XI + CHEEK_T                            # cheek outer face
GROOVE_X = LOWER_FLANGE + FLOOR_W / 2 - WHEEL_W / 2   # the line runs here, and the shaft sits over it
BOARD_Z = PIVOT_Z + PIVOT_DROP               # plywood underside
CROSS_Z = BOARD_Z + BOARD_T + CROSS_ABOVE
LOADED_TILT = math.degrees(math.asin(FLOOR_R / PIVOT_Z))  # swing under a straight-down load
LINE_N = 44.5            # 10 lb
