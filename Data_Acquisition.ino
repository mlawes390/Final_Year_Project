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

union Elapsed{
  unsigned long t_f;
  byte t_b[4];
}Elapsed ;

union x_acel{
  float x_f;
  byte x_b[4];
}x_acel;

union y_acel{
  float y_f;
  byte y_b[4];
}y_acel;

union z_acel{
  float z_f;
  byte z_b[4];
}z_acel;

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
        Elapsed.t_f = micros() - startTime;
        lis.read();
        x_acel.x_f = lis.x_g;
        y_acel.y_f = lis.y_g;
        z_acel.z_f = lis.z_g;
        Serial.write(Elapsed.t_b, 4);
        Serial.write(x_acel.x_b, 4);
        Serial.write(y_acel.y_b, 4);
        Serial.write(z_acel.z_b, 4);
      }
    }
  }
  delay(10);
}

