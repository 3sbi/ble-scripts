import asyncio
import time
from bleak import BleakScanner
import csv
import os.path


def create_file_with_header():
    header = ['name', 'address', 'rssi', 'timestamp_in_ms']
    with open('./bleak-scan-data.csv', 'w', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(header)

def save_to_csv(row: list[str]):
    # open the file in the write mode
    file_exists=os.path.isfile("./bleak-scan-data.csv")
    if (not file_exists):
        create_file_with_header()
    with open('./bleak-scan-data.csv', 'a', encoding='UTF8', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(row)

async def main():
    async with BleakScanner() as scanner:
        print("Scanning...")
        async for device, ad in scanner.advertisement_data():
            if ("VEGA" in device.name):
                save_to_csv([device.name,device.address,ad.rssi,time.time()*1000])
                print(ad._field_defaults, ad._fields);
                print(f'Name: {device.name}, Address: {device.address}, RSSI: {ad.rssi}, time: {time.time()}')
        print("---")


if __name__ == "__main__":
    asyncio.run(main())