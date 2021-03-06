import os
import subprocess
import shlex
import re
import schedule
import time
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


def acquisition(config):
    """
    Poll accelerometer, store collected data in .csv file and process data to produce
    time domain and frequency domain figures and parameters.
    """
    data_directory = config['data-directory']

    start = datetime.datetime.now()
    start_str = start.strftime('%Y-%m-%d_%H:%M:%S')
    print('Sampling Sequence Start {}'.format(start_str))

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


def upload_file(src, dest):
    """
    Upload a single file located (locally) at `src` to `dest`.
    """
    cmd = 'rsync --archive --compress {} {}'.format(src, dest)
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd)
    proc.wait()
    return proc.returncode


def upload(config):
    """
    Upload collected and processed data to a cloud server. Data older than
    two days will be removed from master node.
    """
    login_details = config['repo']
    DESTINATION = '{}@{}:{}'.format(login_details['user'],
                                    login_details['host'],
                                    login_details['path'])

    # Assume data is saved to /path/to/data/
    data_directory = config['data-directory']
    data_files = os.listdir(data_directory)

    print('Uploading Files')

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
    config = {
        'data-directory': './Accelerometer_data',
        'repo': {
            'user': 'matt',
            'host': '128.199.153.103',
            'path':'/home/matt/Vib_data/'
        }
    }

    schedule.every(15).minutes.do(acquisition, config)
    schedule.every().day.at("18:00").do(upload, config)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        #end read when keyboard interrupt
        print('Program end: User interrupt')
        sys.exit(0)


if __name__ == "__main__":
    main()
