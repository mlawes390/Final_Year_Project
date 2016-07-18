#!/usr/bin/env python

import serial
import struct
import csv
import time

port = '/dev/ttyUSB0'
baud = 9600

savefile = '/home/matthew/Desktop/Unprocessed data/test.csv'

ser = serial.Serial(port, baud)
time.sleep(10)
ser.write('s')

with open(savefile, 'wb') as f:
	writer = csv.writer(f)
	while 1:
		raw = ser.read(16)
		data = struct.unpack('Ifff',raw)
		writer.writerow(data)
