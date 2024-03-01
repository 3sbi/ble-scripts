import os
import csv
from bleak import BleakScanner
import time
from datetime import datetime
from util.consts import ADDRESSES

def create_file_with_header(filename:str):
    header = ['datetime_utc', 'address', 'rssi', 'timestamp_in_seconds']
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)

def save_to_csv(filename:str, row: list[str|datetime|float]):
    # open the file in the write mode
    file_exists=os.path.isfile(filename)
    if (not file_exists):
        create_file_with_header(filename)
    with open(filename, 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(row)


# scans N samples and save them to csv file
# filename_ending is used to create different filenames easily if we are collecting multiple samples
async def collect(n_finish:int, filename_ending: str):
    n = 0
    filename: str = f'./data/test0_rssi_for_different_distance/{n_finish}_samples_{filename_ending}.csv'
    async with BleakScanner() as scanner:
        print("Scanning...")
        async for device, advertisement_data in scanner.advertisement_data():
            address = device.address.upper()
            # save device it dict if it's address is in VEGA addresses list
            if (address in ADDRESSES):
                utc = datetime.now()
                timestamp = time.time()
                rssi = advertisement_data.rssi
                print(f'№{n+1} - Time in UTC: {utc}, Address: {address}, RSSI: {rssi}, timestamp: {timestamp}')
                save_to_csv(filename, [utc, address, rssi, timestamp])
                n += 1
                if n == n_finish:
                    print(f"finished collecting {n} samples")
                    break

