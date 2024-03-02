import csv
import matplotlib.pyplot as plt
import numpy as np
import glob


import matplotlib.pyplot as plt
import numpy as np
import os

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


def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def plot_distance_to_rssi_correlation():
    plt.figure()
    plt.grid()
    x = []
    y = []
    filenames = glob.glob("./data/test0_rssi_for_different_distance/3000_samples_*m.csv")
    for filename in filenames:
        print(filename)
        m = filename.replace("./data/test0_rssi_for_different_distance\\3000_samples_",'').replace('m.csv','')
        data: np.NDArray[int] = np.asarray(get_rssis(filename))
        data = reject_outliers(data)
        mean = np.mean(data)
        x.append(m)
        y.append(mean)
    plt.plot(x, y, "go-")
    plt.xlabel('distance, m')
    plt.ylabel('RSSI')
    plt.show()
    return

def plot_occurrence_frequency():
    m = 1
    fig, axes = plt.subplots(nrows=2, ncols=2)
    for ax in axes.flatten():     
        filename = f"./data/test0_rssi_for_different_distance/3000_samples_{m}m.csv"
        data = np.asarray(get_rssis(filename))
        ax.hist(data, bins=np.arange(data.min(), data.max()+1))
        ax.set_title(f'{m} m. from beacon')
        m += 1
    plt.show()