# Final_Year_Project
Data Acquisition and processing scripts for a wireless RDAQ for Vibration condition monitoring

Master node is a Raspberry Pi.
Sensor node is an ATmega328 with STMicroelectronics LIS3DH accelerometer

Usage (Master Node)
-----

Retrieve local copy of code with::

    git clone https://github.com/mlawes390/Final_Year_Project.git

May need to add user to `dialout` group to access serial ports::

    sudo usermod -a -G dialout $USER
  
Data Acquisition requires `PySerial` and `Docopt`. Install with::
  
    pip3 install pyserial docopt

Processing requires `numpy`, `scipy` and `matplotlib`. Install with::

    sudo apt-get install python-scipy python-numpy python-matplotlib



Usage (Sensor Node)
-----

Retrieve local copy of code with::

    git clone https://github.com/mlawes390/Final_Year_Project.git

Retrieve Adafruit LIS3DH libraries from::

    https://github.com/adafruit/Adafruit_LIS3DH

LIS3DH connected via hardware SPI with the chip select pin as Digital Pin 10
