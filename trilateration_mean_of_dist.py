import csv
import numpy as np
from consts import *
from util import trilateration, calc_dist

# test 1
REAL_POSITION = (9.5, 7)
FILENAME = './test1/bluepy-scan-data.csv'

# test 2
# REAL_POSITION = (3.9, 2)
# FILENAME = './test2/bluepy-scan-data.csv'


def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else np.zeros(len(d))
    return data[s<m]

def determine_position(csv_file: str):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        dist_ap24 = []
        dist_ap25 = []
        dist_ap26 = []
        for row in reader:
            if ADDRESSES[0] in row['address']:
                rssi = int(row['rssi'])
                dist = calc_dist(rssi, RSSI_AT_1M, n=N)
                dist_ap24.append(dist) 
                
            if ADDRESSES[1] in row['address']:
                rssi = int(row['rssi'])
                dist = calc_dist(rssi, RSSI_AT_1M, n=N)
                dist_ap25.append(dist) 
                
            if ADDRESSES[2] in row['address']:
                rssi = int(row['rssi'])
                dist = calc_dist(rssi, RSSI_AT_1M, n=N)
                dist_ap26.append(dist) 

        # convert to numpy array
        dist_ap24 = np.array(dist_ap24)
        dist_ap25 = np.array(dist_ap25)
        dist_ap26 = np.array(dist_ap26)


        mean_dist_ap24 = np.nanmean((np.array(dist_ap24)))
        mean_dist_ap25 = np.nanmean((np.array(dist_ap25)))
        mean_dist_ap26 = np.nanmean((np.array(dist_ap26)))

        # print("RSSI values for each beacon:")
        # print(f"AP24 = {dist_ap24}")
        # print(f"AP25 = {dist_ap25}")
        # print(f"AP26 = {dist_ap26}")

        print("\nMean values without outliners:")
        print(f"AP24={float(mean_dist_ap24)}, AP25={float(mean_dist_ap25)}, AP26={float(mean_dist_ap26)} \n")
        dist_values = [float(mean_dist_ap24), float(mean_dist_ap25), float(mean_dist_ap26)]

        # Determine the Squared Root Error and the Mean Squared Error 
        position = trilateration(REF_POINTS, dist_values)
        print(f"Position: {position}")
        print(f"Real position: {REAL_POSITION}")

        SQE = np.sqrt((position[0] - REAL_POSITION[0])**2 + (position[1] - REAL_POSITION[1])**2)
        MSE = np.mean(SQE)
        print(f"SQE={SQE}, MSE={MSE}");
        

determine_position(FILENAME)