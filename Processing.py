#!/usr/bin/env python3
"""
Reads accererometer data .csv file and processes

Usage: Processing.py [options]

Options:
    -i=READ_FILE           The file to read from [Default: ./data.csv
    -h --help              Show this help information
    -V --version           Print the version information
"""
__version__ = '0.1.0'

import time
import sys
import docopt

import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

def main(args):
    read_file = args.get('-i', './data.csv')
    
    #Read input file into a numpy array
    acel_data = np.genfromtxt(read_file, delimiter=",")
    
    #carry out conversions (microseconds to seconds, g to m/s^2)
    acel_data[:,0] = acel_data[:,0]/1000000
    acel_data[:,1:3] = acel_data[:,1:3]*9.81
    
    #Define Frequency parameters
    n = len(acel_data[:,0])             #Length of signal
    k = np.arange(n)
    Fs = n/(acel_data[n-1,0]-acel_data[0,0])
    T = n/Fs
    freq = k/T
    freq = freq[range(n/2)]
    
    #Compute fft (removing DC component)
    X_fft = scipy.fftpack.fft(acel_data[:,1])/n
    X_fft = 2.0/n*np.abs(X_fft[1:n/2])
    Y_fft = scipy.fftpack.fft(acel_data[:,2])/n
    Y_fft = 2.0/n*np.abs(Y_fft[1:n/2])
    Z_fft = scipy.fftpack.fft(acel_data[:,3])/n
    Z_fft = 2.0/n*np.abs(Z_fft[1:n/2])
    
    #Compute Cepstrum
    #X_ceps = np.ifft(np.log(X_fft))
    #Y_ceps = np.ifft(np.log(Y_fft))
    #Z_ceps = np.ifft(np.log(Z_fft))
    
    
    #Plot Time Domain
    plt.subplot (3,1,1)
    plt.plot (acel_data[:,0], acel_data[:,1], '-b', label='X axis')
    plt.plot (acel_data[:,0], acel_data[:,2], '-r', label='Y axis')
    plt.plot (acel_data[:,0], acel_data[:,3], '-g', label='Y axis')
    plt.title('Time Domain')
    plt.legend()
    plt.xlabel('Time (s)')
    ply.ylabel('Acceleration (m/s^2)')
    
    #Plot Frequency Domain
    plt.subplot (3,1,2)
    plt.plot (freq[1:], X_fft, '-b', label='X axis')
    plt.plot (freq[1:], Y_fft, '-r', label='Y axis')
    plt.plot (freq[1:], Z_fft, '-g', label='Z axis')
    plt.title('Frequency Domain')
    plt.legend()
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    
    #Plot Cepstrum Analysis
    
    
if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    #print(args)
    main(args) 
    
    
    
