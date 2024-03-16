import csv
import numpy as np
import math
from util.consts import ADDRESSES
from util.util_func import remove_outliers, trilateration


# for cases when there is only 3 beacons in one room
def determine_position_static(csv_filename: str, real_position: tuple[float, float], serial_to_ref_position: dict[int, tuple[float, float]]):
    beacon_serial_numbers: list[int] = list(serial_to_ref_position.keys())
    ref_points: list[tuple[float, float]] = list(serial_to_ref_position.values())
    beacon_addresses: list[str] = []
    for num in beacon_serial_numbers:
        address = ADDRESSES.get(num)
        if (address):
            beacon_addresses.append(address)
    
    beacon_0_rssis: list[int] = []
    beacon_1_rssis: list[int] = []
    beacon_2_rssis: list[int] = []
    with open(csv_filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            index: int = beacon_addresses.index(row['address'])
            if index == 0:
                beacon_0_rssis.append(int(row['rssi']))
            if index == 1:
                beacon_1_rssis.append(int(row['rssi']))
            if index == 2:
                beacon_2_rssis.append(int(row['rssi']))
        # beacon_0_rssis = remove_outliers(np.array(beacon_0_rssis)).tolist()
        # beacon_1_rssis = remove_outliers(np.array(beacon_1_rssis)).tolist()
        # beacon_2_rssis = remove_outliers(np.array(beacon_2_rssis)).tolist()
        rssi_values = [float(np.nanmean(np.array(beacon_0_rssis))), float(np.nanmean(np.array(beacon_1_rssis))), float(np.nanmean(np.array(beacon_2_rssis)))]
        print(f'RSSI values={rssi_values}')
        
        # Determine the Squared Root Error and the Mean Squared Error 
        position = trilateration(ref_points, rssi_values)
        print(f"Calculated position: {position}")
        print(f"Real position: {real_position}")

        SQE = math.sqrt((position[0] - real_position[0])**2 + (position[1] - real_position[1])**2)
        MSE = np.mean(SQE)
        print(f"SQE={SQE}, MSE={MSE}")


