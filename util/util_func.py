from util.consts import RSSI_AT_1M, N 
import numpy as np


def calc_dist(rssi: float, rssi_at_1m: int | float, n: int) -> float:
    cal_d= pow(10,((rssi_at_1m - rssi)/(10*n)))
    return cal_d


def trilateration(ref_points: list[tuple[float, float]], rssi_values: list[int] | list[float]) -> tuple[float, float]:
    # Extract reference point coordinates and RSSI values
    (x1, y1), (x2, y2), (x3, y3) = ref_points
    rssi_1, rssi_2, rssi_3 = rssi_values

    # Calculate distances from RSSI values using the log-distance path loss model
    d1 = calc_dist(rssi_1, RSSI_AT_1M, N)
    d2 = calc_dist(rssi_2, RSSI_AT_1M, N)
    d3 = calc_dist(rssi_3, RSSI_AT_1M, N)

    # Calculate trilateration coefficients
    A = 2 * x2 - 2 * x1
    B = 2 * y2 - 2 * y1
    C = d1**2 - d2**2 - x1**2 + x2**2 - y1**2 + y2**2
    D = 2 * x3 - 2 * x2
    E = 2 * y3 - 2 * y2
    F = d2**2 - d3**2 - x2**2 + x3**2 - y2**2 + y3**2

    # Calculate position coordinates
    x = (C*E - F*B) / (A*E - B*D)
    y = (C*D - A*F) / (B*D - A*E)
    return x, y



def remove_outliers(data: np.ndarray, m: float = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]
