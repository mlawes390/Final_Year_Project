import os
import subprocess
import shlex
import re
import datetime

def gen_filename(rfcomm, now):
    """
    Generate file name for rfcomm with timestamp.
    """
    match = re.search(r'\d+', rfcomm)
    if match is None:
        raise ValueError('Invalid rfcomm, {}'.format(rfcomm))

    port = match.group(0)
    now_str = now.strftime('%Y-%m-%d_%H:%M:%S')

    filename = 'Acel_{}_{}.csv'.format(port, now_str)
    return filename


def rfcomms():
    """
    Get a list of all rfcomm on the system.
    """
    ports = []
    for device in os.listdir('/dev/'):
        if device.startswith('rfcomm'):
            ports.append('/dev/' + device)
    return ports


def main():
    """
    Poll accelerometer, store collected data in .csv file and process data to produce
    time domain and frequency domain figures and parameters.
    """
    data_directory = './Accelerometer_data'

    count = 1

    for rfcomm in rfcomms():
        now = datetime.datetime.now()
        filename = gen_filename(rfcomm, now)
        full_name = os.path.join(data_directory, filename)

        # Poll sensor and save to .csv
        print('Sampling {}'.format(count))
        cmd = 'python3 Data_Acquisition.py -o {} -p {}'.format(full_name, rfcomm)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()

        # Process data
        print('Processing {}'.format(count))
        cmd = 'python3 Processing.py -o {}'.format(full_name)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()

        count += 1

if __name__ == "__main__":
    main()
