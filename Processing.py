#!/usr/bin/env python3
"""
Reads accelerometer data .csv file and generates plots of time domain, frequency
domain, and cepstrum analysis. Time domain is analysed and results stored in a
.txt file

Usage: Processing.py [options]

Options:
    -o=READ_FILE           The file to read from [Default: ./test.csv]
    -h --help              Show this help information
    -V --version           Print the version information
"""
__version__ = '0.1.0'

import os
import sys
import docopt
import warnings

import math
import numpy as np
from numpy.fft import ifft
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import constants
import scipy.stats


def write_td(t, ax, mean, g_rms, v_rms, p2v, cst, kts):
    t.write("\n")
    t.write(ax + " Axis" + "\n")
    t.write("Mean (m/s^2): " + str(mean) + "\n")
    t.write("G RMS (g): " + str(g_rms) + "\n")
    t.write("V RMS (m/s): " + str(v_rms) + "\n")
    t.write("Peak to valley (m/s^2): " + str(p2v) + "\n")
    t.write("Crest Factor: " + str(cst) + "\n")
    t.write("Kurtosis: " + str(kts) + "\n")


def main(args):
    read_file = args.get('-o', './test.csv')
    (path, extension) = os.path.splitext(read_file)

    warnings.simplefilter('error', UserWarning)

    # Read input file into a numpy array
    while True:
        try:
            acel_data = np.genfromtxt(read_file, delimiter=",")
            break
        except UserWarning:
            print("Error: Empty input file")
            sys.exit(0)

    # carry out conversions (microseconds to seconds, g to m/s^2)
    acel_data[:, 0] = acel_data[:, 0] / 1000000
    acel_data[:, 1:] = acel_data[:, 1:] * constants.g

    # Define Frequency parameters
    n = len(acel_data[:, 0])  # Length of signal
    k = np.arange(n)
    fs = n / (acel_data[n - 1, 0] - acel_data[0, 0])
    t = n / fs
    freq = k / t
    freq = freq[range(int(n / 2))]

    # Compute fft and single sided amplitude spectrum
    acel_f = np.zeros((n,3))
    acel_f[:, 0] = np.abs(fft(acel_data[:, 1]))
    x_am = np.abs(acel_f[:, 0][range(int(n / 2))] / n)
    acel_f[:,1] = np.abs(fft(acel_data[:, 2]))
    y_am = np.abs(acel_f[:, 1][range(int(n / 2))] / n)
    acel_f[:,2] = np.abs(fft(acel_data[:, 3]))
    z_am = np.abs(acel_f[:, 2][range(int(n / 2))] / n)

    # Compute real Cepstrum
    x_ceps = np.real(ifft(np.log(acel_f[:, 0])))
    y_ceps = np.real(ifft(np.log(acel_f[:, 1])))
    z_ceps = np.real(ifft(np.log(acel_f[:, 2])))

    # Divide acceleration data by frequency to obtain velocity data
    bin_num_a = np.arange(0,n/2,1)
    bin_num_b = np.arange(n/2,0,-1)
    bin_num = np.append(bin_num_a,bin_num_b)
    f_bin = 2*np.pi*bin_num*fs/n

    with np.errstate(divide='ignore'):
        vel_f = acel_f / f_bin[:, None]


    # Apply 3 Hz filter
    n_df = 3
    nfilt = math.floor(n_df/(fs/n))
    vel_f[0:nfilt, :] = 0
    vel_f[n-nfilt:n, :] = 0

    #
    vel_data = np.zeros((n,3))
    vel_data[:, 0] = np.real(ifft(vel_f[:, 0]))
    vel_data[:, 1] = np.real(ifft(vel_f[:, 1]))
    vel_data[:, 2] = np.real(ifft(vel_f[:, 2]))

    plt.figure(figsize=(12.8, 7.2), dpi=100)
    # Plot Time Domain
    plt.subplot(3, 1, 1)
    plt.plot(acel_data[:, 0], acel_data[:, 1], '-b', label='X axis')
    plt.plot(acel_data[:, 0], acel_data[:, 2], '-r', label='Y axis')
    plt.plot(acel_data[:, 0], acel_data[:, 3], '-g', label='Z axis')
    plt.title('Time Domain')
    plt.legend(loc=1, fontsize=10)
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s^2)')

    # Plot Frequency Domain
    plt.subplot(3, 1, 2)
    plt.plot(freq[1:], x_am[1:], '-b', label='X axis')
    plt.plot(freq[1:], y_am[1:], '-r', label='Y axis')
    plt.plot(freq[1:], z_am[1:], '-g', label='Z axis')
    plt.yscale('log')
    plt.title('Frequency Domain')
    plt.legend(loc=1, fontsize=10)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    # Plot Cepstrum Analysis
    plt.subplot(3, 1, 3)
    plt.plot(acel_data[:, 0], x_ceps, '-b', label='X axis')
    plt.plot(acel_data[:, 0], y_ceps, '-r', label='Y axis')
    plt.plot(acel_data[:, 0], z_ceps, '-g', label='Z axis')
    plt.title('Real Cepstrum Analysis')
    plt.legend(loc=1, fontsize=10)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude (dB)')

    # Save figure
    plt.tight_layout()
    plt.savefig(path + '.png', format='png')

    # Calculate Time Domain parameters (in m/s^2)
    ax = ('X', 'Y', 'Z')
    mean = np.mean(acel_data[:, 1:], axis=0)
    min_ = np.amin(acel_data[:, 1:], axis=0)
    max_ = np.amax(acel_data[:, 1:], axis=0)
    p2v = max_ - min_
    grms = np.sqrt(np.mean(np.square(acel_data[:, 1:]), axis=0)) / constants.g
    vrms = np.sqrt(np.mean(np.square(vel_data), axis=0))
    cst = p2v / grms
    kts = scipy.stats.kurtosis(acel_data[:, 1:])

    # Write time domain parameters to text file
    with open(path + '.txt', 'w') as t:
        t.write("Sample time (sec): " + str(acel_data[n - 1, 0]) + "\n")
        t.write("Number of Samples: " + str(n) + "\n")
        t.write("Sample rate (Hz): " + str(fs) + "\n")
        for i in range(3):
            write_td(t, ax[i], mean[i], grms[i], vrms[i], p2v[i], cst[i], kts[i])


if __name__ == '__main__':
    args = docopt.docopt(__doc__, version=__version__)
    # print(args)
    main(args)
