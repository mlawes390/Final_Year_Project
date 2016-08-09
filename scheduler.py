import os
import re
import schedule
import time
import datetime


def generate_filename(rfcomm, now):
    match = re.search(r'\d+', rfcomm)
    if match is None:
        raise ValueError('Invalid rfcomm, {}'.format(rfcomm))

    port = match.group(0)
    now_str =now.strftime('%Y-%m-%d_%H:%M:%S')

    filename = 'accel_{}_{}.csv'.format(port, now_str)
    return filename

def rfcomms():
    """
    Get a list of all the rfcomms on the system.
    """
    ports = []
    for device in os.listdir('/dev/'):
        if device.startswith('/dev/rfcomm'):
            ports.append(device)
    return ports


def acquisition():
    for rfcomm in rfcomms():
        now = datetime.datetime.now()
        filename = generate_filename(rfcomm, now)



def upload():
    print('Uploading stuff')



def main():
    schedule.every(15).minutes.do(acquisition)
    schedule.every().day.at('18:00').do(upload)

    while True:
        schedule.run_pending()
        time.sleep(1)




if __name__ == '__main__':
    main()
