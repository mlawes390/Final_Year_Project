/* Author: M.LAWES
   Curtin University of Technology
   Final Year Project 2016

   Accelerometer Data Acquisition between Arduino Nano Sensor node and Paspberry Pi Master Node
*/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>

#define LIS3DH_CS 10
// Hardware SPI
Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);

void setup(void) {
  Serial.begin(9600);

  lis.begin();
  lis.setRange(LIS3DH_RANGE_4_G);                 // 2, 4, 8 or 16 G!
  lis.setDataRate (LIS3DH_DATARATE_LOWPOWER_1K6HZ);  //POWERDOWN, 1_HZ, 10_HZ, 25_HZ, 50_HZ, 100_HZ 200_HZ, 400_HZ, LOWPOWER_1K6HZ, LOWPOWER_5KHZ
}

void loop() {
  if (Serial.available()) {

    byte r = Serial.read();

    if (r == (byte)'s') {
      unsigned long startTime = micros();
      for (int i = 0; i < 100; i++) {
        unsigned long elapsedTime = micros() - startTime;
        lis.read();
        sendStream(elapsedTime, lis.x_g, lis.y_g, lis.z_g);
      }
    }
  }
  delay(10);
}

void sendStream(unsigned long elapsedTime, float X_g, float Y_g, float Z_g) {
  byte * t = (byte *) &elapsedTime;
  byte * x = (byte *) &X_g;
  byte * y = (byte *) &Y_g;
  byte * z = (byte *) &Z_g;

  Serial.write(t[0]);
  Serial.write(t[1]);
  Serial.write(t[2]);
  Serial.write(t[3]);
  Serial.write(x[0]);
  Serial.write(x[1]);
  Serial.write(x[2]);
  Serial.write(x[3]);
  Serial.write(y[0]);
  Serial.write(y[1]);
  Serial.write(y[2]);
  Serial.write(y[3]);
  Serial.write(z[0]);
  Serial.write(z[1]);
  Serial.write(z[2]);
  Serial.write(z[3]);
}
