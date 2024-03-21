import csv
from matplotlib import pyplot as plt
import numpy as np
import math
import pandas as pd
from util.consts import (
    ADDRESSES,
    APPLY_KALMAN_TO_TRILATERATION,
    APPLY_RELATIVE_METERS,
    IMAGE_ON_BACKGROUND_PLOT,
)
from util.kalman import KalmanFilter
from util.relative_meters_method import relative_meters_method
from util.util_func import add_origin, trilateration


# https://stackoverflow.com/questions/23199796/detect-and-exclude-outliers-in-a-pandas-dataframe
def remove_outliers(data: list[int]) -> list[int]:
    df = pd.DataFrame(data)
    q_low = df[0].quantile(0.01)
    q_hi = df[0].quantile(0.99)
    df_filtered = df[(df[0] < q_hi) & (df[0] > q_low)]
    return df_filtered[0].tolist()


# for cases when there is only 3 beacons in one room
def determine_position_static_for_median(
    csv_filename: str,
    real_position: tuple[float, float],
    serial_to_ref_position: dict[int, tuple[float, float]],
):
    beacon_serial_numbers: list[int] = list(serial_to_ref_position.keys())
    ref_points: list[tuple[float, float]] = list(serial_to_ref_position.values())
    beacon_addresses: list[str] = []
    for num in beacon_serial_numbers:
        address = ADDRESSES.get(num)
        if address:
            beacon_addresses.append(address)
    beacon_0_rssis: list[int] = []
    beacon_1_rssis: list[int] = []
    beacon_2_rssis: list[int] = []
    position = (0, 0)
    with open(csv_filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            index: int = beacon_addresses.index(row["address"])
            if index == 0:
                beacon_0_rssis.append(int(row["rssi"]))
            if index == 1:
                beacon_1_rssis.append(int(row["rssi"]))
            if index == 2:
                beacon_2_rssis.append(int(row["rssi"]))

        rssi_values = [
            float(np.median(np.array(beacon_0_rssis))),
            float(np.median(np.array(beacon_1_rssis))),
            float(np.median(np.array(beacon_2_rssis))),
        ]
        print(f"RSSI values={rssi_values}")

        # Determine the Squared Root Error and the Mean Squared Error
        if APPLY_RELATIVE_METERS:
            print("Applying relative meters method...")
            position = relative_meters_method(ref_points, rssi_values)
        else:
            print("Applying basic trilateration to RSSI values...")
            position = trilateration(ref_points, rssi_values)
        print(f"Calculated position: {position}")
        print(f"Real position: {real_position}")

        SQE = math.sqrt(
            (position[0] - real_position[0]) ** 2
            + (position[1] - real_position[1]) ** 2
        )
        MSE = np.mean(SQE)
        print(f"SQE={SQE}, MSE={MSE}")
    plot_static_position_and_mse(
        csv_filename,
        real_position,
        ref_points,
        calculated_meadian_position=position,
    )


def plot_static_position_and_mse(
    csv_filename: str,
    real_position: tuple[float, float],
    ref_points: list[tuple[float, float]],
    calculated_meadian_position: tuple[float, float],
):
    positions: list[tuple[float, float]] = []
    timestamps: list[str] = []
    kf_x = KalmanFilter(0.001, 0.2)
    kf_y = KalmanFilter(0.001, 0.2)
    with open(csv_filename, "r") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for row in rows:
            timestamp = row["timestamp_in_seconds"]
            if timestamp in timestamps:
                continue
            else:
                timestamps.append(timestamp)
                matches = [
                    row for row in rows if row["timestamp_in_seconds"] == timestamp
                ]
                rssi_values = [int(o["rssi"]) for o in matches]
                if APPLY_RELATIVE_METERS:
                    position: tuple[float, float] | None = relative_meters_method(
                        ref_points, rssi_values
                    )
                    if position is None:
                        continue
                else:
                    position: tuple[float, float] = trilateration(
                        ref_points, rssi_values
                    )
                    if position is None:
                        continue
                    if APPLY_KALMAN_TO_TRILATERATION:
                        position = (kf_x.filter(position[0]), kf_y.filter(position[1]))
                if position[0] < 0:
                    position = (0, position[1])
                if position[1] < 0:
                    position = (position[0], 0)
                positions.append(position)
    # plot scatter plot for each position
    plt.figure()
    plt.grid()
    x = [pos[0] for pos in positions]
    y = [pos[1] for pos in positions]
    scatter = plt.scatter(x, y)
    if IMAGE_ON_BACKGROUND_PLOT:
        img = plt.imread("./data/room.png")
        plt.imshow(img, extent=[0, 9.5, 0, 8])
        positions = [add_origin(position) for position in positions]
        real_position = add_origin(real_position)
    real_scatter = plt.scatter(real_position[0], real_position[1], color="red")
    calc_scatter = plt.scatter(
        calculated_meadian_position[0], calculated_meadian_position[1], color="lime"
    )
    plt.legend(
        (real_scatter, calc_scatter, scatter),
        (
            "Реальное местоположение",
            "Трилатерация по медиане",
            "Трилатерация по каждой точке",
        ),
    )
    plt.show()

    # plot changing MSE fro each position
    x_timestamps = [float(t) for t in timestamps]
    MSEs: list[float] = []
    for position in positions:
        SQE = math.sqrt(
            (position[0] - real_position[0]) ** 2
            + (position[1] - real_position[1]) ** 2
        )
        MSE = np.mean(SQE)
        MSEs.append(MSE)
    plt.figure()
    plt.plot(x_timestamps, MSEs)
    plt.xlabel("Время, мсек", fontdict={"fontsize": 20})
    plt.ylabel("MSE", fontdict={"fontsize": 20})
    plt.title("Изменение MSE по времени")
    plt.show()
