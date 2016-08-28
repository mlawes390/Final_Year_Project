#!/usr/bin/env python3
"""
Reads accelerometer data sent through via the sensor node and
saves as a .csv file

Usage: Data_Acquisition.py [options]

Options:
    -o=SAVE_FILE           The file to write to [Default: ./data.csv]
    -b=BAUD --baud=BAUD    The Baud Rate [Default: 115200]
    -p=PORT --port=PORT    The serial port to listen to [Default: /dev/ttyUSB0]
    -t=TIMEOUT --timeout=TIMEOUT
                           Set the timeout for the read operation [Default: 5]
    -h --help              Show this help information
    -V --version           Print the version information
"""
__version__ = '0.1.0'

import serial
import struct
import csv
import time
import sys
import docopt

def main(args):
    save_file = args.get('-o', './data.csv')

    # Open serial connection with node
    ser = serial.Serial(args['--port'],
                        baudrate=int(args['--baud']),
                        timeout=int(args['--timeout']))
    # Allow time for serial to initlise and send start byte
    time.sleep(10)

    # open .csv file with write
    with open(save_file, 'w') as f:
        writer = csv.writer(f)
        ser.write(b's')
        try:
            while True:
                raw = ser.read(16)
                if len(raw)==0:
                    print('Program End')
                    sys.exit(0)
                data = struct.unpack('Ifff',raw)
                writer.writerow(data)
        except KeyboardInterrupt:
            # end read when keyboard interrupt
            print('Program end: User interrupt')
            sys.exit(0)

if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    #print(args)
    main(args)
