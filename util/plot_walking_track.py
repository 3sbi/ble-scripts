import csv
import matplotlib.pyplot as plt
import numpy as np
from util.consts import ADDRESSES, N, RSSI_AT_1M
from util.util_func import trilateration 

def plot_track(positions: list[tuple[float, float]], real_positions:  list[tuple[float, float]]):
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    x_real = [pos[0] for pos in real_positions]
    y_real = [pos[1] for pos in real_positions]
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u/2
    pos_y = y[:-1] + v/2
    norm = np.sqrt(u**2+v**2)
    plt.plot(x, y, marker="o", label="track")
    plt.plot(x_real, y_real, label='real')
    plt.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid")
    plt.legend()
    plt.title("Трек перемещения")
    plt.show()


def get_ref_points_by_addresses(addresses: list[str], all_ref_points: dict[int, tuple[float, float]]):
    ref_points = []
    for address in addresses:
        index = list(ADDRESSES.values()).index(address)
        ref_point_number = list(ADDRESSES.keys())[index]
        point = all_ref_points.get(ref_point_number)
        ref_points.append(point)
    return ref_points


def plot_walking_track(csv_filename: str, all_ref_points: dict[int, tuple[float, float]], real_positions:  list[tuple[float, float]]):
    timestamps = []
    positions = []
    with open(csv_filename, 'r') as file:
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
                addresses = [o['address'] for o in matches]
                ref_points = get_ref_points_by_addresses(addresses, all_ref_points)
                position: tuple[float, float] = trilateration(ref_points, rssi_values, RSSI_AT_1M, N)
                if position[0] < 0:
                    position =(0, position[1])
                if position[1] < 0:
                    position =(position[0], 0)
                positions.append(position)
    plot_track(positions, real_positions)