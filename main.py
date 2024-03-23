import asyncio
from collect_data.async_scanner import scan
from collect_data.collect_n_samples import collect
from util.draw import (
    plot_occurrence_frequencies_for_different_beacons,
    plot_occurrence_frequency,
    plot_distance_to_rssi_correlation,
    plot_rssi_to_time,
)
from get_coords.determine_static_position import determine_position_static_for_median
from get_coords.plot_walking_track import plot_walking_track
import time


def main():
    mode = input(
        "\nEnter modes:\n"
        + " 0 - scanning continuously\n"
        + " 01 - get N number of measurements (test 0)\n"
        + " 02 - plot for measurements (test 0)\n"
        + " 03 - plot frequencies for different beacons (test 0) \n"
        + " 1 - print trilateration results (test 1 - on table) \n"
        + " 2 - print trilateration results (test 2 - in corner) \n"
        + " 3 - plot trilateration results (test 3 - move in circle) \n"
        + ' 4 - plot trilateration results (test 4 - "snake") \n'
        + " 5 - plot trilateration results (test 5 - go outside of cabinet) \n"
        + "\nEnter mode: "
    )
    if mode == "0":
        ending: str = input("filename ending: ")
        timer = 5
        while True:
            print(f"Scanning will start in {timer}")
            timer -= 1
            time.sleep(1)
            if timer == 0:
                break
        asyncio.run(scan(ending))
    if mode == "01":
        n_measurements = input("Enter number of measurements: ")
        ending = input("filename ending: ")
        asyncio.run(collect(int(n_measurements), ending))
    if mode == "02":
        subdirectory: str = input("\nEnter subdirectory: ")
        plot_occurrence_frequency(subdirectory)
        plot_distance_to_rssi_correlation(subdirectory)
        plot_rssi_to_time(subdirectory)
    if mode == "03":
        plot_occurrence_frequencies_for_different_beacons()
    if mode == "1":
        filename: str = "./data/test1_on_table/scan_data.csv"
        real_position = (6.5, 1.4)
        ref_points: dict[int, tuple[float, float]] = {
            24: (2, 6.82),
            25: (8.1, 6.82),
            26: (4.75, 0),
        }
        determine_position_static_for_median(filename, real_position, ref_points)
    if mode == "2":
        type = input("old or new? ")

        filename: str = "./data/test2_in_corner/scan_data.csv"
        real_position = (8.5, 6.82)
        ref_points: dict[int, tuple[float, float]] = {
            30: (2, 6.82),
            25: (7.5, 6.82),
            26: (4.75, 0),
        }
        if type == "old":
            filename: str = "./data/test2_in_corner/old_scan_data.csv"
            ref_points: dict[int, tuple[float, float]] = {
                24: (2, 6.82),
                25: (7.5, 6.82),
                26: (4.75, 0),
            }
        determine_position_static_for_median(filename, real_position, ref_points)
    if mode == "3":
        test_number = input("test number: 1, 2 or 3? ")
        filename: str = f"./data/test3_move_in_circle/scan_data_v{test_number}.csv"
        ref_points: dict[int, tuple[float, float]] = {
            24: (2, 6.82),
            25: (7.5, 6.82),
            26: (4.75, 0),
        }
        real_positions: list[tuple[float, float]] = [
            (8.0, 0.7),
            (0.6, 0.7),
            (0.6, 5.82),
            (8.0, 5.82),
            (8.0, 0.7),
        ]
        plot_walking_track(filename, ref_points, real_positions, mode)
    if mode == "4":
        test_number = input("test number: 1 or 2? ")
        filename: str = f"./data/test4_move_snake/scan_data_v{test_number}.csv"
        ref_points: dict[int, tuple[float, float]] = {
            24: (2, 6.82),
            25: (7.5, 6.82),
            26: (4.75, 0),
        }
        if test_number == "2":
            ref_points[30] = ref_points.pop(24)

        real_positions: list[tuple[float, float]] = [
            (8.0, 0.7),
            (8.0, 5.82),
            (0.6, 5.82),
            (0.6, 2.82),
            (7.8, 2.82),
            (7.8, 0.7),
        ]
        plot_walking_track(filename, ref_points, real_positions, mode)
    if mode == "5":
        test_number = input("test number: 1, 2 or 3? ")
        filename: str = (
            f"./data/test5_go_outside_of_cabinet/scan_data_v{test_number}.csv"
        )
        real_positions: list[tuple[float, float]] = [
            (10.43, 5.82),
            (0.5, 4.51),
            (0.5, 0.5),
            (1.93, 0.5),
            (1.93, 4.51),
            (3.43, 4.51),
            (3.43, 0.7),
            (10.43, 0.7),
        ]
        ref_points: dict[int, tuple[float, float]] = {
            22: (2.43, 2.87),
            24: (0, 0),
            25: (9.93, 6.82),
            26: (7.18, 0),
            30: (4.43, 6.82),
        }
        plot_walking_track(filename, ref_points, real_positions, mode)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
