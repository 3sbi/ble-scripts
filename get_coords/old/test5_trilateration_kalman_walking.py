import numpy as np
import csv
import matplotlib.pyplot as plt
from util.consts import *
from util.util_func import trilateration
from util.kalman import KalmanFilter

#test 5
FILENAME = './data/test5/timeout-5s-v2/bleak-scan-data.csv'

# значения местоположения маяков для тестов 4, 5
TEST5_REF_POINTS = {
    22: (0, 3),
    24: (7.2, 3.4),
    25: (11.85, 10.6),
    26: (1.03, 11.89),
    30: (6.45, 8.7)
}

def get_ref_points_by_addresses(addresses):
    ref_points = []
    for address in addresses:
        index = list(ADDRESSES.values()).index(address)
        ref_point_number = list(ADDRESSES.keys())[index]
        point = TEST5_REF_POINTS.get(ref_point_number)
        ref_points.append(point)
    return ref_points

def plot_sqe_graph(SQEs):
    plt.plot(range(len(SQEs)), SQEs, label= "SQE")
    mean_value = np.nanmean((np.array(SQEs)))
    plt.plot(range(len(SQEs)), [mean_value]*len(SQEs), label="mean SQE")
    plt.legend()
    plt.show()

def plot_track(positions):
    x = [pos[0] for pos in positions]
    y=  [pos[1] for pos in positions]
    
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u/2
    pos_y = y[:-1] + v/2
    norm = np.sqrt(u**2+v**2)
    plt.plot(x, y, marker="o", label="track")
    plt.plot([10, 2.5, 2.5, 10],[6, 6, 10, 10],label='real')
    plt.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid")
    plt.legend()
    plt.title("Трек перемещения")
    plt.show()


def determine_position(csv_file: str):
    kf = KalmanFilter(0.001, 0.2)
    kf_x = KalmanFilter(0.001, 0.2)
    kf_x.x = 10
    kf_y = KalmanFilter(0.001, 0.2)
    kf_y.x = 6
    timestamps = []
    positions = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            timestamp = row['timestamp_in_seconds']
            if timestamp in timestamps:
                continue
            else:
                timestamps.append(timestamp)
                matches = [row for row in rows if row['timestamp_in_seconds'] == timestamp]
                rssi_values = [int(o['rssi']) for o in matches]
                # predictions=[]
                # for measurement in rssi_values:
                #     predictions.append(kf.filter(measurement))
                # rssi_values = predictions
                addresses = [o['address'] for o in matches]
                ref_points = get_ref_points_by_addresses(addresses)
                # Determine the Squared Root Error and the Mean Squared Error 
                position = trilateration(ref_points, rssi_values, RSSI_AT_1M, N)
                position = (kf_x.filter(position[0]), kf_y.filter(position[1]))
                if position[0] < 0:
                    position =(0, position[1])
                if position[1] < 0:
                    position =(position[0], 0)
                positions.append(position)
                print(f"Calculated position: {position}")
    plot_track(positions)



determine_position(FILENAME)