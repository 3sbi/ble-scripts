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
import time
from datetime import datetime

timeout = 10.0
filename = './bleak-scan-data.csv'

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
    print("bleak: scanning for 10 seconds, please wait...")

    devices = await BleakScanner.discover(timeout,
        return_adv=True, cb=dict(use_bdaddr=args.macos_use_bdaddr)
    )

    for device, adv in devices.values():
        if ("VEGA" in device.name):
            values = [datetime.now(), device.address.upper(), adv.rssi, time.time()]
            print(f'Time in UTC: {values[0]}, Address: {values[1]}, RSSI: {values[2]}, timestamp: {values[3]}')
            save_to_csv(values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--macos-use-bdaddr",
        action="store_true",
        help="when true use Bluetooth address instead of UUID on macOS",
    )

    args = parser.parse_args()
    while True:
        asyncio.run(main(args))