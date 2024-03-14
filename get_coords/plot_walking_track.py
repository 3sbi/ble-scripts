import csv
import matplotlib.pyplot as plt
import numpy as np
from util.consts import ADDRESSES, N, RSSI_AT_1M, ADDRESS_AP30, ADDRESS_AP22, ADDRESS_AP24, ADDRESS_AP25, ADDRESS_AP26
from util.kalman import KalmanFilter
from util.util_func import trilateration, relative_meters_method

def add_plot_with_quivers(positions:list[tuple[float, float]], color: str, label:str):
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    u = np.diff(x)
    v = np.diff(y)
    pos_x = x[:-1] + u/2
    pos_y = y[:-1] + v/2
    norm = np.sqrt(u**2+v**2)
    print(u)
    print(norm)
    print(u/norm)
    print(v/norm)
    plt.plot(x, y, marker="o", label=label, color=color)
    plt.quiver(pos_x, pos_y, u/norm, v/norm, angles="xy", zorder=5, pivot="mid", color=color, headwidth=2, headlength=5)


def plot_track(positions: list[tuple[float, float]], real_positions:  list[tuple[float, float]]):
    add_plot_with_quivers(positions=positions, color="#1f77b4", label="track")
    add_plot_with_quivers(positions=real_positions, color="orange", label="real")
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


def plot_walking_track(csv_filename: str, all_ref_points: dict[int, tuple[float, float]], real_positions:  list[tuple[float, float]], test_num: str):
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
                addresses = [o['address'] for o in matches]
                if (test_num == '5'):
                    if not (ADDRESS_AP24 in addresses and ADDRESS_AP22 in addresses):
                        if (ADDRESS_AP30 in addresses or ADDRESS_AP26 in addresses or ADDRESS_AP25 in addresses) and (ADDRESS_AP24 in addresses or ADDRESS_AP22 in addresses):
                            continue
                rssi_values = [int(o['rssi']) for o in matches]
                addresses = [o['address'] for o in matches]
                ref_points = get_ref_points_by_addresses(addresses, all_ref_points)
                position: tuple[float, float] = trilateration(ref_points, rssi_values)
                
                # position = (kf_x.filter(position[0]), kf_y.filter(position[1]))
                if position[0] < 0:
                    position =(0, position[1])
                if position[1] < 0:
                    position =(position[0], 0)
                positions.append(position)
    plot_track(positions, real_positions)


def plot_walking_track_relative_meters(csv_filename: str, all_ref_points: dict[int, tuple[float, float]], real_positions:  list[tuple[float, float]], test_num: str):
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
                addresses = [o['address'] for o in matches]
                if (test_num == '5'):
                    if not (ADDRESS_AP24 in addresses and ADDRESS_AP22 in addresses):
                        if (ADDRESS_AP30 in addresses or ADDRESS_AP26 in addresses or ADDRESS_AP25 in addresses) and (ADDRESS_AP24 in addresses or ADDRESS_AP22 in addresses):
                            continue
                rssi_values = [int(o['rssi']) for o in matches]
                addresses = [o['address'] for o in matches]
                ref_points = get_ref_points_by_addresses(addresses, all_ref_points)
                position: tuple[float, float]|None = relative_meters_method(ref_points, rssi_values)
                if (position is None):
                    continue
                if position[0] < 0:
                    position = (0, position[1])
                if position[1] < 0:
                    position = (position[0], 0)
                positions.append(position)
    plot_track(positions, real_positions)