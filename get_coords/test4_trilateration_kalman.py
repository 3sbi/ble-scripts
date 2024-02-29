import math
import numpy as np
import csv
import matplotlib.pyplot as plt
from consts import *
from util import trilateration

#test 4
REAL_POSITION = (5.95, 2)
FILENAME = './test4/bleak-scan-data.csv'

# значения местоположения маяков для тестов 4, 5
TEST4_REF_POINTS = {
    22: (0, 3),
    24: (7.2, 3.4),
    25: (11.85, 10.6),
    26: (1.03, 11.89),
    30: (6.45, 8.7)
}

class KalmanFilter:
    cov = float('nan')
    x = float('nan')

    def __init__(self, R, Q):
        """
        Constructor
        :param R: Process Noise
        :param Q: Measurement Noise
        """
        self.A = 1
        self.B = 0
        self.C = 11111

        self.R = R
        self.Q = Q

    def filter(self, measurement):
        """
        Filters a measurement
        :param measurement: The measurement value to be filtered
        :return: The filtered value
        """
        u = 0
        if math.isnan(self.x):
            self.x = (1 / self.C) * measurement
            self.cov = (1 / self.C) * self.Q * (1 / self.C)
        else:
            predX = (self.A * self.x) + (self.B * u)
            predCov = ((self.A * self.cov) * self.A) + self.R

            # Kalman Gain
            K = predCov * self.C * (1 / ((self.C * predCov * self.C) + self.Q));

            # Correction
            self.x = predX + K * (measurement - (self.C * predX));
            self.cov = predCov - (K * self.C * predCov);

        return self.x

    def last_measurement(self):
        """
        Returns the last measurement fed into the filter
        :return: The last measurement fed into the filter
        """
        return self.x

    def set_measurement_noise(self, noise):
        """
        Sets measurement noise
        :param noise: The new measurement noise
        """
        self.Q = noise

    def set_process_noise(self, noise):
        """
        Sets process noise
        :param noise: The new process noise
        """
        self.R = noise

# class KalmanFilter(object):
#     def __init__(self, F = None, B = None, H = None, Q = None, R = None, P = None, x0 = None):

#         if(F is None or H is None):
#             raise ValueError("Set proper system dynamics.")

#         self.n = F.shape[1]
#         self.m = H.shape[1]

#         self.F = F
#         self.H = H
#         self.B = 0 if B is None else B
#         self.Q = np.eye(self.n) if Q is None else Q
#         self.R = np.eye(self.n) if R is None else R
#         self.P = np.eye(self.n) if P is None else P
#         self.x = np.zeros((self.n, 1)) if x0 is None else x0

#     def predict(self, u = 0):
#         self.x = np.dot(self.F, self.x) + np.dot(self.B, u)
#         self.P = np.dot(np.dot(self.F, self.P), self.F.T) + self.Q
#         return self.x

#     def update(self, z):
#         y = z - np.dot(self.H, self.x)
#         S = self.R + np.dot(self.H, np.dot(self.P, self.H.T))
#         K = np.dot(np.dot(self.P, self.H.T), np.linalg.inv(S))
#         self.x = self.x + np.dot(K, y)
#         I = np.eye(self.n)
#         self.P = np.dot(np.dot(I - np.dot(K, self.H), self.P), 
#         	(I - np.dot(K, self.H)).T) + np.dot(np.dot(K, self.R), K.T)

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
        index = list(DICT_ADDRESSES.values()).index(address)
        ref_point_number = list(DICT_ADDRESSES.keys())[index]
        point = TEST4_REF_POINTS.get(ref_point_number)
        ref_points.append(point)
    return ref_points


def determine_position(csv_file: str):
    kf = KalmanFilter(0.001, 0.2)
    kf_position_x = KalmanFilter(0.001, 0.2)
    kf_position_y = KalmanFilter(0.001, 0.2)
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