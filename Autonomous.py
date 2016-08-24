import os
import subprocess
import shlex
import re
import scheduler
import time
import datetime
import dropbox


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
        if device.startswith('/dev/rfcomm'):
            ports.append(device)
    return ports


def acquisition():
    """
    Poll accelerometer, store collected data in .csv file and process data to produce
    time domain and frequency domain figures and parameters.
    """
    for rfcomm in rfcomms():
        now = datetime.datetime.now()
        filename = gen_filename(rfcomm, now)

        # Poll sensor and save to .csv
        cmd = 'python3 Data_acquisition.py -o {} -p {}'.format(filename, rfcomm)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()

        # Process data
        cmd = 'python3 processing.py -o {}'.format(filename)
        cmd = shlex.split(cmd)
        proc = subprocess.Popen(cmd)
        proc.wait()


def upload_file(src, dest):
    """
    Upload a single file located (locally) at `src` to `dest`.
    """
    cmd = 'rsync --archive --compress {} {}'.format(src, dest)
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd)
    proc.wait()
    return proc.returncode


def upload():
    """
    Upload collected and processed data to a cloud server. Data older than
    two days will be removed from master node.
    """
    DESTINATION = 'matt@example.com:/var/daq-uploads'

    # Assume data is saved to /path/to/data/
    # TODO: Change the path to the data folder or make sure it's set with
    # configuration
    data_directory = '/path/to/data/'
    data_files = os.listdir(data_directory)

    # Iterate through data files, uploading them one at a time and then
    # Deleting the file if upload was successful
    for data_file in data_files:
        full_name = os.path.join(data_directory, data_file)
        ret = upload_file(full_name, DESTINATION)

        if ret != 0:
            print('Error occurred while uploading {}'.format(full_name))
        else:
            os.remove(full_name)


def main():
    schedule.every(15).minutes.do(acquisition)
    schedule.every().day.at("18:00").do(upload)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
