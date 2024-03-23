ADDRESS_AP22 = "F3:B0:D4:A4:42:E0"
ADDRESS_AP24 = "D7:AB:60:ED:B3:66"
ADDRESS_AP25 = "E9:71:D6:A6:52:19"
ADDRESS_AP26 = "FA:A5:6E:E8:3D:9C"
ADDRESS_AP30 = "E4:02:B8:34:EC:F3"
ADDRESS_AP241 = "EE:93:45:01:28:95"
ADDRESS_AP265 = "C0:11:E6:96:20:A0"

ADDRESSES = {
    22: "F3:B0:D4:A4:42:E0",
    24: "D7:AB:60:ED:B3:66",
    25: "E9:71:D6:A6:52:19",
    26: "FA:A5:6E:E8:3D:9C",
    30: "E4:02:B8:34:EC:F3",
    241: "EE:93:45:01:28:95",
    265: "C0:11:E6:96:20:A0",
}

N = 3
RSSI_AT_1M: float = -49

# Значения местоположения маяков для тестов 1, 2, 3
# Define reference points with known positions and RSSI values
TEST123_REF_POINT_AP24 = (2, 7)
TEST123_REF_POINT_AP25 = (7.50, 7)
TEST123_REF_POINT_AP26 = (4.75, 0)

IMAGE_ON_BACKGROUND_PLOT = True
ORIGIN_FOR_BG_IMAGE = (0.35, 0.41)

DRAW_LABELS_WITH_RSSI_VALUES = False

APPLY_RELATIVE_METERS = False
APPLY_KALMAN_TO_TRILATERATION = False
# APPLY_REMOVE_OUTLINERS = True
