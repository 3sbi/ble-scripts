from bluepy.btle import Scanner
import os
import csv
import time
from datetime import datetime

timeout = 10.0
filename = './bluepy-scan-data.csv'
ble_beacons_addrs = ['FA:A5:6E:E8:3D:9C', 'E9:71:D6:A6:52:19', 'D7:AB:60:ED:B3:66']

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
        #5.0 sec scanning
        print("bluepy: scanning for 10 seconds, please wait...")
        ble_list = Scanner().scan(timeout)

        for dev in ble_list:
            if (dev.addr.upper() in ble_beacons_addrs):
                values = [datetime.now(), dev.addr.upper(), dev.rssi, time.time()]
                print(f"Time in UTC: {values[0]}, Address: {values[1]}, RSSI: {values[2]},  Timestamp: {values[3]}")
                save_to_csv(values)
    except:
        raise Exception("Error occured")