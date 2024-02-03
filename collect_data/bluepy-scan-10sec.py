from bluepy.btle import Scanner
import os
import csv
import time
from consts import *
from datetime import datetime

timeout = 3.0
filename = './bluepy-scan-data.csv'

def create_file_with_header():
    header = ['datetime_utc', 'address', 'rssi', 'timestamp_in_seconds']
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)

def save_to_csv(row: list[str]):
    # open the file in the write mode
    file_exists=os.path.isfile(filename)
    if (not file_exists):
        create_file_with_header()
    with open(filename, 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(row)


while True:
    try:     
        print(f"{datetime.now()} | bluepy: scanning for {timeout} seconds, please wait...")
        ble_list = Scanner().scan(timeout)
        global discovered_devices_addresses

        for device in ble_list:
            if (device.addr.upper() in ADDRESSES):
                print(f'found beacon with address: {device.address.upper()}')
                discovered_devices_addresses[device.address.upper()] = (device.rssi)

        if len(discovered_devices_addresses.keys()) >= 3:
            print(discovered_devices_addresses)
            print("\nFOUND 3 OR MORE, WRITING TO FILE")
            delta_rssi_addresses = {} 
            for address in discovered_devices_addresses:
                delta_rssi_addresses[address] = abs(discovered_devices_addresses[address]-RSSI_AT_1M)
            smallest_deltas_addresses = sorted(delta_rssi_addresses, key=delta_rssi_addresses.get)[:3]
            print(smallest_deltas_addresses)

            utc = datetime.now()
            timestamp = time.time()
            for address in smallest_deltas_addresses:
                rssi = discovered_devices_addresses[address]
                values = [utc, address, rssi, timestamp]
                print(f'Time in UTC: {values[0]}, Address: {values[1]}, RSSI: {values[2]}, timestamp: {values[3]}')
                save_to_csv(values)
            print('')
            discovered_devices_addresses = {}

    except:
        raise Exception("Error occured")