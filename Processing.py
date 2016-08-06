#!/usr/bin/env python3
"""
Reads accererometer data .csv file and processes

Usage: Processing.py [options]

Options:
    -i=READ_FILE           The file to read from [Default: ./data.csv]
    -h --help              Show this help information
    -V --version           Print the version information
"""
__version__ = '0.1.0'

import time
import sys
import os
import docopt

import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
import scipy.stats

def main(args):
    read_file = args.get('-i', './data.csv')
    (path, extension) = os.path.splitext(read_file)
    
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
    
    #Compute fft and single sided amplitude spectrum (removing DC component)
    X_fft = np.abs(scipy.fftpack.rfft(acel_data[:,1]))
    X_am = np.abs(X_fft[range(n/2)]/n)
    Y_fft = np.abs(scipy.fftpack.rfft(acel_data[:,2]))
    Y_am = np.abs(Y_fft[range(n/2)]/n)
    Z_fft = np.abs(scipy.fftpack.rfft(acel_data[:,3]))
    Z_am = np.abs(Z_fft[range(n/2)]/n)
    
    #Compute real Cepstrum
    X_ceps = np.real(np.fft.ifft(np.log(X_fft)))
    Y_ceps = np.real(np.fft.ifft(np.log(Y_fft)))
    Z_ceps = np.real(np.fft.ifft(np.log(Z_fft)))
    
    #Plot Time Domain
    plt.subplot (3,1,1)
    plt.plot (acel_data[:,0], acel_data[:,1], '-b', label='X axis')
    plt.plot (acel_data[:,0], acel_data[:,2], '-r', label='Y axis')
    plt.plot (acel_data[:,0], acel_data[:,3], '-g', label='Y axis')
    plt.title('Time Domain')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')
    
    #Plot Frequency Domain
    plt.subplot (3,1,2)
    plt.plot (freq[1:], X_am[1:], '-b', label='X axis')
    plt.plot (freq[1:], Y_am[1:], '-r', label='Y axis')
    plt.plot (freq[1:], Z_am[1:], '-g', label='Z axis')
    plt.title('Frequency Domain')
    plt.legend()
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    
    #Plot Cepstrum Analysis
    plt.subplot (3,1,3)
    plt.plot (acel_data[:,0], X_ceps, '-b', label='X axis')
    plt.plot (acel_data[:,0], Y_ceps, '-r', label='Y axis')
    plt.plot (acel_data[:,0], Z_ceps, '-g', label='Y axis')
    plt.title('Real Cepstrum Analysis')
    plt.legend()
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (dB)')
    
    #Save figure
    plt.tight_layout()
    plt.savefig(path, format='png')
    
    #Calculate Velocity Time Domain
    
    #Calculate Time Domain parameters (in m/s^2)
    X_mean = np.mean(acel_data[:,1])
    X_min = np.amin(acel_data[:,1])
    X_max = np.amax(acel_data[:,1])
    X_p2v = X_max - X_min
    X_rms = np.sqrt(np.mean(np.square(acel_data[:,1])))
    X_cst = X_p2v/X_rms
    X_kts = scipy.stats.kurtosis(acel_data[:,1]
    
    #Write time domain parameters to text file
    with open(path + '.txt','w') as t:
        t.write("Sample time (sec): " + str(acel_data[n-1,0]) + "\n")
        t.write("Number of Samples: " +str(n) + "\n")
        t.write("Sample rate (Hz): " + str(Fs) + "\n")
        t.write("\n")
        t.write("X Axis" + "\n")
        t.write("Mean (m/s^2): " + str(X_mean) + "\n")
        t.write("G RMS (m/s^2): " + str(X_rms) + "\n")
        t.write("Peak to valley (m/s^2): " + str(X_p2v) + "\n")
        t.write("Crest Factor: " + str(X_cst) + "\n")
        t.write('Kurtosis: " + str(X_kts) + "\n")
    
    
if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    #print(args)
    main(args) 
    
    
    
