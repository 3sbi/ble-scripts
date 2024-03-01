import asyncio
from calendar import c
from collect_data.async_scanner import scan
from collect_data.collect_n_samples import collect
from util.draw import plot_occurrence_frequency

def main():
    mode = input("\nEnter modes:\n" +
                 " 1 - scanning continuously\n" + 
                 " 2 - get N number of measurements (test 0)\n" +
                 " 3 - plot for measurements (test 0)\n" +
                 "\nEnter mode: ")
    if mode == '1':
        asyncio.run(scan())
    if mode == '2':
        n_measurements = input('Enter number of measurements: ')
        ending = input('filename ending: ')
        asyncio.run(collect(int(n_measurements),ending))
    if mode == '3':
        plot_occurrence_frequency()
        


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass