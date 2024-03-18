import csv
import matplotlib.pyplot as plt
import numpy as np
import glob
import math
from util.consts import N, RSSI_AT_1M
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
    x: list[str] = []
    y = []
    filenames = glob.glob(f'./data/test0_rssi_to_distance_correlation/{subdirectory}/*.csv')
    for filename in filenames:
        meters = filename.split('_samples_').pop().replace("m.csv", '')
        data = np.array(get_rssis(filename))
        data = remove_outliers(data)
        rssi = np.median(data)
        x.append(meters)
        y.append(rssi)
    plt.plot(x, y, "go-", label="Медианное значение с тестовые данных")
    
    y_real = []
    for value in x:
        distance = int(value)
        rssi = -10 * N * math.log10(distance) + RSSI_AT_1M
        y_real.append(rssi)

    plt.plot(x, y_real, "yo-", label="значение по формуле rssi=-10*N*log10(distance)+RSSI_AT_1M")
    plt.xlabel('Расстояние, м.', fontdict={"fontsize":20})
    plt.ylabel('RSSI', fontdict={"fontsize":20})
    plt.title('Корреляция')
    plt.legend()
    plt.show()
    return

def plot_rssi_to_time(subdirectory: str):
    plt.figure()
    x = []
    y = []
    timestamp: float = 0
    filename = glob.glob(f'./data/test0_rssi_to_distance_correlation/{subdirectory}/*_3m.csv')[0]
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            if (i < 120):
                continue
            if (i == 120):
                timestamp = float(row['timestamp_in_seconds'])
            if i > 190:
                break
            x.append(float(row['timestamp_in_seconds']) - timestamp)
            y.append(int(row['rssi']))
    plt.plot(x, y)
    plt.xlabel('Время, сек', fontdict={"fontsize": 20})
    plt.ylabel('RSSI', fontdict={"fontsize": 20})
    plt.show()
    return

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
        count: int = 0
        if m == 1:
            count = np.count_nonzero(data < 60) + np.count_nonzero(np.logical_and(data > -56, data < -53)) + np.count_nonzero(data >  -49)
        if m == 2:
            count = np.count_nonzero(data < -48) + np.count_nonzero(data > -44)
        if m == 3:
            count = np.count_nonzero(data < -72) + np.count_nonzero(np.logical_and(data > -68, data < -48)) + np.count_nonzero(data > -59)
        if m == 4:
            count = np.count_nonzero(data < -82) + np.count_nonzero(np.logical_and(data > -77, data < -74)) + np.count_nonzero(data > 68)
        print(f'Выбросов на {m} м. от маяка: {count / len(data):.4f}%')
        ax.hist(data, bins=np.arange(data.min(), data.max()+1))
        ax.set_title(f'{m} м. от маяка')
    plt.show()


def plot_rssi_for_beacon(signal): 
    signal_gray_filter = gray_filter(signal, N=8)
    signal_fft_filter = fft_filter(signal, N=10, M=2)
    signal_kalman_filter = kalman_filter(signal, A=1, H=1, Q=1.6, R=6)
    signal_particle_filter = particle_filter(signal, quant_particles=100, A=1, H=1, Q=1.6, R=6)
    plot_signals([signal, signal_gray_filter, signal_fft_filter, signal_kalman_filter, signal_particle_filter],
                ['signal', 'gray_filtered_signal', 'fft_filtered_signal', 'kalman_filtered_signal',
                'particles_filtered_signal'])
    

def plot_occurrence_frequencies_for_different_beacons():
    filenames = glob.glob(f'./data/test0_rssi_to_distance_correlation/balcony/3000_samples_3m*.csv')
    fig, axes = plt.subplots(nrows=1, ncols=len(filenames))
    for index, ax in enumerate(axes.flatten()):
        filename = filenames[index]
        data = np.asarray(get_rssis(filename))
        ax.hist(data, bins=np.arange(data.min(), data.max()+1))
        ax.xaxis.set_ticks(np.arange(min(data), max(data)+1, 1.0))
        title = 'Маяк #30' if 'beacon30' in filename else 'Маяк #26'
        if ('beacon22' in filename):
            title = 'Маяк #22'
        ax.set_title(title, fontdict={"fontsize": 20})
    fig.suptitle("Распределение RSSI на 3м. для разных маяков", fontsize=20)
    plt.show()