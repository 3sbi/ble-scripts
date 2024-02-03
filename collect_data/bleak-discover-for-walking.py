"""
Scan/Discovery
--------------

Example showing how to scan for BLE devices.

Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""
import argparse
import asyncio
import os
import csv
from bleak import BleakScanner
from consts import *
import time
from datetime import datetime

timeout = 5.0
filename = './bleak-scan-data.csv'
discovered_devices_addresses: dict = {}

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

async def main(args: argparse.Namespace):
    print(f"{datetime.now()} | bleak: scanning for {timeout} seconds, please wait...")
    global discovered_devices_addresses
    devices = await BleakScanner.discover(timeout,
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )
    
    for device, adv in devices.values():
        if (device.address in ADDRESSES):
            print(f'found beacon with address: {device.address.upper()}')
            discovered_devices_addresses[device.address.upper()] = (adv.rssi)

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
        print('\n')
        discovered_devices_addresses = {}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()
    try:
        while True:
            asyncio.run(main(args))
    except KeyboardInterrupt:
        pass