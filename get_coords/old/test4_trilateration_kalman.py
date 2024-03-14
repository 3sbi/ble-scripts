import math
import numpy as np
import csv
import matplotlib.pyplot as plt
from util.consts import *
from util.kalman import KalmanFilter
from util.util_func import trilateration

#test 4
REAL_POSITION = (5.95, 2)
FILENAME = './data/test4/bleak-scan-data.csv'

# значения местоположения маяков для тестов 4, 5
TEST4_REF_POINTS = {
    22: (0, 3),
    24: (7.2, 3.4),
    25: (11.85, 10.6),
    26: (1.03, 11.89),
    30: (6.45, 8.7)
}

def plot_predictions(title, measurements, predictions):
    plt.plot(range(len(measurements)), measurements, label = 'Measurements')
    plt.plot(range(len(predictions)), np.array(predictions), label = 'Kalman Filter Prediction')
    plt.legend()
    plt.title(title)
    plt.show()

def get_predictions(measurements):
    kf = KalmanFilter(0.001, 0.15)
    predictions = []
    for measurement in measurements:
        predictions.append(kf.filter(measurement))
    return predictions

def get_predictions_and_plot(measurements, name):
    predictions = get_predictions(measurements)[7:]
    measurements = measurements[7:]
    plot_predictions(name, measurements, predictions)
    return measurements, predictions

def get_ref_points_by_addresses(addresses):
    ref_points = []
    for address in addresses:
        index = list(ADDRESSES.values()).index(address)
        ref_point_number = list(ADDRESSES.keys())[index]
        point = TEST4_REF_POINTS.get(ref_point_number)
        ref_points.append(point)
    return ref_points


def determine_position(csv_file: str):
    kf = KalmanFilter(0.02, 0.15)
    timestamps = []
    sqes = []
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
                predictions=[]
                for measurement in rssi_values:
                    predictions.append(kf.filter(measurement))
                rssi_values = predictions
                addresses = [o['address'] for o in matches]
                print(addresses)
                ref_points = get_ref_points_by_addresses(addresses)
                # Determine the Squared Root Error and the Mean Squared Error 
                position = trilateration(ref_points, rssi_values, RSSI_AT_1M, N)
                print(f"Calculated position: {position}")
                print(f"Real position: {REAL_POSITION}")
                SQE = math.sqrt((position[0] - REAL_POSITION[0])**2 + (position[1] - REAL_POSITION[1])**2)
                sqes.append(SQE)
                MSE = np.mean(SQE)
                print(f"SQE={SQE}, MSE={MSE}\n");
    plt.plot(range(len(sqes)), sqes, label= "SQE")
    mean_value = np.nanmean((np.array(sqes)))
    plt.plot(range(len(sqes)), [mean_value]*len(sqes), label="mean SQE")
    plt.legend()
    plt.show()


determine_position(FILENAME)