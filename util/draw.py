import csv
import matplotlib.pyplot as plt
import numpy as np
import glob
import matplotlib.pyplot as plt
import numpy as np
import math

from util.filters import gray_filter, fft_filter, kalman_filter, particle_filter
from util.util_func import remove_outliers

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


def get_rssis(filename: str) -> list[int]:
    values: list[int] = []
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            values.append(int(row['rssi']))
    return values


def plot_distance_to_rssi_correlation(subdirectory: str):
    plt.figure()
    plt.grid()
    x = []
    y = []
    filenames = glob.glob(f'./data/test0_rssi_to_distance_correlation/{subdirectory}/*.csv')
    for filename in filenames:
        m = filename.split('_samples_').pop().replace("m.csv", '')
        data = np.array(get_rssis(filename))
        data = remove_outliers(data)
        rssi = np.mean(data)
        x.append(m)
        y.append(rssi)
    plt.plot(x, y, "go-")
    plt.xlabel('distance, m')
    plt.ylabel('RSSI')
    plt.title('Correlation')
    plt.show()
    return

# y = −0.0556x3+1.0120x2−7.3196x−46.8543

def plot_occurrence_frequency(subdirectory: str):
    filenames = glob.glob(f'./data/test0_rssi_to_distance_correlation/{subdirectory}/*.csv')
    filenames.sort()
    ncols = math.ceil(len(filenames)/2)
    fig, axes = plt.subplots(nrows=2, ncols=ncols)
    for index, ax in enumerate(axes.flatten()):
        filename = filenames[index]
        m = index + 1
        if index > len(filenames)-1 and (len(filenames) % 2) != 0:
            continue
        data = np.asarray(get_rssis(filename))
        ax.hist(data, bins=np.arange(data.min(), data.max()+1))
        ax.set_title(f'{m} m. from beacon')
    plt.show()


def plot_rssi_for_beacon(signal): 
    signal_gray_filter = gray_filter(signal, N=8)
    signal_fft_filter = fft_filter(signal, N=10, M=2)
    signal_kalman_filter = kalman_filter(signal, A=1, H=1, Q=1.6, R=6)
    signal_particle_filter = particle_filter(signal, quant_particles=100, A=1, H=1, Q=1.6, R=6)
    plot_signals([signal, signal_gray_filter, signal_fft_filter, signal_kalman_filter, signal_particle_filter],
                ['signal', 'gray_filtered_signal', 'fft_filtered_signal', 'kalman_filtered_signal',
                'particles_filtered_signal'])