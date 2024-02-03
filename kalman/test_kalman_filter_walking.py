import math
import numpy as np
import csv
import matplotlib.pyplot as plt
from consts import *
from util import trilateration

#test walking 1
REAL_POSITION = (5.95, 2)
FILENAME = './walking/test1/bleak-scan-data.csv'

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
        self.C = 1

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
    for m in measurements:
        predictions.append(kf.filter(m))
    return predictions

def get_predictions_and_plot(measurements, name):
    predictions = get_predictions(measurements)[7:]
    measurements = measurements[7:]
    plot_predictions(name, measurements, predictions)
    return measurements, predictions


def determine_position(csv_file: str):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rssi_ap22 = []
        rssi_ap24 = []
        rssi_ap25 = []
        rssi_ap26 = []
        rssi_ap30 = []
        for row in reader:
            if ADDRESS_AP22 in row['address']:
                value = int(row['rssi'])
                rssi_ap22.append(value) 

            if ADDRESS_AP24 in row['address']:
                value = int(row['rssi'])
                rssi_ap24.append(value) 
                
            if ADDRESS_AP25 in row['address']:
                value = int(row['rssi'])
                rssi_ap25.append(value)
                
            if ADDRESS_AP26 in row['address']:
                value = int(row['rssi'])
                rssi_ap26.append(value)

            if ADDRESS_AP30 in row['address']:
                value = int(row['rssi'])
                rssi_ap30.append(value) 


        # convert to numpy array
        rssi_ap24 = np.array(rssi_ap24)
        rssi_ap25 = np.array(rssi_ap25)
        rssi_ap26 = np.array(rssi_ap26)
        
        # apply kalman filter
        (rssi_ap24, filtered_rssi_ap24) = get_predictions_and_plot(rssi_ap24, 'ap24')
        (rssi_ap25, filtered_rssi_ap25) = get_predictions_and_plot(rssi_ap25, 'ap25')
        (rssi_ap26, filtered_rssi_ap26) = get_predictions_and_plot(rssi_ap26, 'ap26')

        mean_rssi_ap24 = np.nanmean((np.array(filtered_rssi_ap24)))
        mean_rssi_ap25 = np.nanmean((np.array(filtered_rssi_ap25)))
        mean_rssi_ap26 = np.nanmean((np.array(filtered_rssi_ap26)))

        print("\nMean values:")
        print(f"AP24={float(mean_rssi_ap24)}, AP25={float(mean_rssi_ap25)}, AP26={float(mean_rssi_ap26)}")
        rssi_values = [float(mean_rssi_ap24), float(mean_rssi_ap25), float(mean_rssi_ap26)]
        ref_points = [REF_POINT_AP24, REF_POINT_AP25, REF_POINT_AP22]

        # Determine the Squared Root Error and the Mean Squared Error 
        position = trilateration(ref_points, rssi_values, RSSI_AT_1M, N)
        print(f"\nCalculated position: {position}")
        print(f"Real position: {REAL_POSITION}")

        SQE = math.sqrt((position[0] - REAL_POSITION[0])**2 + (position[1] - REAL_POSITION[1])**2)
        MSE = np.mean(SQE)
        print(f"SQE={SQE}, MSE={MSE}");


determine_position(FILENAME)