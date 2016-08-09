import datetime
from scheduler import generate_filename

def test_generate_filename():
    rfcomm = '/dev/rfcomm1'
    now = datetime.datetime.now()
    should_be = 'accel_1_{}.csv'.format(now.strftime('%Y-%m-%d_%H:%M:%S'))

    got = generate_filename(rfcomm, now)
    assert got == should_be


def test_rfcomms():
    pass
