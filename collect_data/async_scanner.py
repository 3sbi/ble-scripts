import os
import csv
from bleak import BleakScanner
import time
from datetime import datetime
from util.consts import ADDRESSES, RSSI_AT_1M

filename = './bleak-scan-data.csv'
discovered_devices_addresses: dict[str, int] = {}

def create_file_with_header():
    header = ['datetime_utc', 'address', 'rssi', 'timestamp_in_seconds']
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)

def save_to_csv(row: list[str|datetime|float]):
    # open the file in the write mode
    file_exists=os.path.isfile(filename)
    if (not file_exists):
        create_file_with_header()
    with open(filename, 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(row)


# scans and saves collected data to csv file
async def scan():
    async with BleakScanner() as scanner:
        print("Scanning...")
        global discovered_devices_addresses
        async for device, advertisement_data in scanner.advertisement_data():
            address = device.address.upper()
            # save device it dict if it's address is in listed VEGA addresses
            if (address in ADDRESSES):
                print(f'found beacon with address={address} and RSSI={advertisement_data.rssi}')
                discovered_devices_addresses[address] = (advertisement_data.rssi)
            # 3+ devices is enough for triangulation

            if len(discovered_devices_addresses.keys()) >= 3:
                print("\nFOUND 3 OR MORE BEACONS, WRITING TO FILE")
                delta_rssi_addresses: dict[str, int] = {} 
                for address in discovered_devices_addresses:
                    delta_rssi_addresses[address] = abs(discovered_devices_addresses[address]-RSSI_AT_1M)
                
                # process only data for the three devices closest to the user
                smallest_deltas_addresses: list[str] = sorted(delta_rssi_addresses, key=delta_rssi_addresses.get)[:3]         # type: ignore
                utc = datetime.now()
                timestamp = time.time()
                for address in smallest_deltas_addresses:
                    rssi = discovered_devices_addresses[address]
                    print(f'Time in UTC: {utc}, Address: {address}, RSSI: {rssi}, timestamp: {timestamp}')
                    save_to_csv([utc, address, rssi, timestamp])
                print('\n')
                discovered_devices_addresses = {}

