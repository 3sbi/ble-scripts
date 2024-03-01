import matplotlib.pyplot as plt
import numpy as np


def plot_signals(signals, labels):

    """

    Auxiliary function to plot all signals.

    input:
        - signals: signals to plot
        - labels: labels of input signals

    output:
        - display plot

    """

    alphas = [1, 0.45, 0.45, 0.45, 0.45]      # just some opacity values to facilitate visualization

    lenght = np.shape(signals)[1]             # time lenght of original and filtered signals

    plt.figure()

    for j, sig in enumerate(signals):          # iterates on all signals

        plt.plot(range(lenght), sig, '-o', label=labels[j], markersize=2, alpha=alphas[j])

    plt.grid()

    plt.ylabel('RSSI')
    plt.xlabel('time')
    plt.legend()
    plt.show()

    return



def calc_dist(rss, rssi_at_1m, n):
    cal_d= pow(10,((rssi_at_1m - rss)/(10*n)))
    return cal_d


def trilateration(ref_points, rssi_values, rssi_at_1m, n):
    # Extract reference point coordinates and RSSI values
    (x1, y1), (x2, y2), (x3, y3) = ref_points
    r1, r2, r3 = rssi_values


    # Calculate distances from RSSI values using the log-distance path loss model
    d1 = calc_dist(r1, rssi_at_1m, n)
    d2 = calc_dist(r2, rssi_at_1m, n)
    d3 = calc_dist(r3, rssi_at_1m, n)

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