import csv
import numpy as np
import math
from consts import *
from util import trilateration

# test 1
# REAL_POSITION = (9.5, 7)
# FILENAME = './test1/bluepy-scan-data.csv'

# test 2
REAL_POSITION = (3.9, 2)
FILENAME = './test2/bluepy-scan-data.csv'


def determine_position(csv_file: str):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        rssi_ap24 = []
        rssi_ap25 = []
        rssi_ap26 = []
        for row in reader:
            if ADDRESSES[0] in row['address']:
                value = int(row['rssi'])
                rssi_ap24.append(value) 
                
            if ADDRESSES[1] in row['address']:
                value = int(row['rssi'])
                rssi_ap25.append(value)
                
            if ADDRESSES[2] in row['address']:
                value = int(row['rssi'])
                rssi_ap26.append(value)

        mean_rssi_ap24 = np.nanmean(np.array(rssi_ap24))
        mean_rssi_ap25 = np.nanmean(np.array(rssi_ap25))
        mean_rssi_ap26 = np.nanmean(np.array(rssi_ap26))

        print("\nMean values:")
        print(f"AP24={float(mean_rssi_ap24)}, AP25={float(mean_rssi_ap25)}, AP26={float(mean_rssi_ap26)} \n")
        rssi_values = [float(mean_rssi_ap24), float(mean_rssi_ap25), float(mean_rssi_ap26)]

        # Determine the Squared Root Error and the Mean Squared Error 
        position = trilateration(REF_POINTS, rssi_values, RSSI_AT_1M, N)
        print(f"Calculated position: {position}")
        print(f"Real position: {REAL_POSITION}")

        SQE = math.sqrt((position[0] - REAL_POSITION[0])**2 + (position[1] - REAL_POSITION[1])**2)
        MSE = np.mean(SQE)
        print(f"SQE={SQE}, MSE={MSE}");
        

determine_position(FILENAME)