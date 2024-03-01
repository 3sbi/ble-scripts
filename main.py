import asyncio
from calendar import c
from collect_data.async_scanner import scan
from collect_data.collect_n_samples import collect


def scanning_cont():
    try:
        while True:
            asyncio.run(scan())
    except KeyboardInterrupt:
        pass


def main():
    mode = input("\nEnter modes:\n 1 - scanning continuously\n 2 - get N number of measurements\n\nEnter mode: ")
    if mode == '1':
        scanning_cont()
    if mode == '2':
        n_measurements = input('Enter number of measurements: ')
        ending = input('filename ending: ')
        try:
            asyncio.run(collect(int(n_measurements),ending))
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()