import asyncio
from collect_data.async_scanner import scan
from collect_data.collect_n_samples import collect
from util.draw import plot_occurrence_frequency, plot_distance_to_rssi_correlation
from util.trilateration import determine_position_static
import time

def main():
    mode = input("\nEnter modes:\n" +
                 " 0 - scanning continuously\n" + 
                 " 01 - get N number of measurements (test 0)\n" +
                 " 02 - plot for measurements (test 0)\n" +
                 " 1 - print trilateration results (test 1 - on table) \n" +
                 " 2 - print trilateration results (test 2 - in corner) \n" +
                 " 3 - plot trilateration results (test 3 - move in circle) \n" +
                 " 4 - plot trilateration results (test 4 - \"snake\") \n" +
                 " 5 - plot trilateration results (test 5 - go outside of cabinet) \n" +
                 "\nEnter mode: ")
    if mode == '0':
        ending = input('filename ending: ')
        timer = 5
        while True:
            print(f'Scanning will start in {timer}')
            timer -= 1
            time.sleep(1)
            if timer == 0:
                break
        asyncio.run(scan(ending))
    if mode == '01':
        n_measurements = input('Enter number of measurements: ')
        ending = input('filename ending: ')
        asyncio.run(collect(int(n_measurements),ending))
    if mode == '02':
        subdirectory: str = input("\nEnter subdirectory: ")
        plot_occurrence_frequency(subdirectory)
        plot_distance_to_rssi_correlation(subdirectory)
    if mode == '1':
        filename = "./data/test1_on_table/scan_data.csv"
        real_position = (6.5, 1.4)
        ref_points: dict[int,tuple[float, float]] = {
            24: (2, 6.82),
            25: (8.1, 6.82),
            26: (4.75, 0)
        }
        determine_position_static(filename, real_position, ref_points)
    if mode == '2':
        type = input("old or new? ")

        filename = "./data/test2_in_corner/scan_data.csv"
        real_position = (8.5, 6.82)
        ref_points: dict[int,tuple[float, float]] = {
            30: (2, 6.82),
            25: (7.5, 6.82),
            26: (4.75, 0)
        }
        if (type == 'old'):
            filename = "./data/test2_in_corner/old_scan_data.csv"
            ref_points: dict[int,tuple[float, float]] = {
                24: (2, 6.82),
                25: (8.5, 6.82),
                26: (4.75, 0)
            }
        determine_position_static(filename, real_position, ref_points)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
