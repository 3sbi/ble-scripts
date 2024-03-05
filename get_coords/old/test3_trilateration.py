import math
import numpy as np
import csv
from util.consts import TEST123_REF_POINT_AP24, TEST123_REF_POINT_AP25, TEST123_REF_POINT_AP26, RSSI_AT_1M, N, ADDRESSES
from util.util_func import trilateration

REF_POINTS = [TEST123_REF_POINT_AP24, TEST123_REF_POINT_AP25, TEST123_REF_POINT_AP26]

# тест 3 - проход по прямой линии в кабинете 202
# каждые 15 секунд человек проходит 100 см., поэтому реальные позиции именно такие
REAL_POSITIONS = [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1)]
FILENAME = './data/test3/bluepy-scan-data.csv'


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

        # convert to numpy array
        rssi_ap24 = np.array(rssi_ap24)
        rssi_ap25 = np.array(rssi_ap25)
        rssi_ap26 = np.array(rssi_ap26)

        for index in range(0, len(rssi_ap24), 3):
            print("____________________________")
            real_position=REAL_POSITIONS[int(index/3)]
            print(f"Real position: {real_position}")
            segment_ap24 = rssi_ap24[index:index+3]
            segment_ap25 = rssi_ap25[index:index+3]
            segment_ap26 = rssi_ap26[index:index+3]
            
            mean_rssi_ap24 = np.nanmean(np.array(segment_ap24))
            mean_rssi_ap25 = np.nanmean(np.array(segment_ap25))
            mean_rssi_ap26 = np.nanmean(np.array(segment_ap26))
            rssi_values = [float(mean_rssi_ap24), float(mean_rssi_ap25), float(mean_rssi_ap26)]

            # Determine the Squared Root Error and the Mean Squared Error 
            position = trilateration(REF_POINTS, rssi_values, RSSI_AT_1M, N)
            print(f"Calculated position: {position}")

            SQE = math.sqrt((position[0] - real_position[0])**2 + (position[1] - real_position[1])**2)
            MSE = np.mean(SQE)
            print(f"SQE={SQE}, MSE={MSE}");
        

determine_position(FILENAME)