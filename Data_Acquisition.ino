/* Author: M.LAWES
   Curtin University of Technology
   Final Year Project 2016

   Accelerometer Data Acquisition between Arduino Nano Sensor node and Paspberry Pi Master Node
*/

#include <Wire.h>
#include <SPI.h>
#include <avr/interrupt.h>
#include <avr/power.h>
#include <avr/sleep.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <MatrixMath.h>


#define LIS3DH_CS 10
// Hardware SPI
Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);

int pin2 = 2;
int count=0;
union Elapsed {
  unsigned long t_f;
  byte t_b[4];
} Elapsed ;

union x_acel {
  float x_f;
  byte x_b[4];
} x_acel;

union y_acel {
  float y_f;
  byte y_b[4];
} y_acel;

union z_acel {
  float z_f;
  byte z_b[4];
} z_acel;

float cal_mat[4][3] = {{1, 0, 0},
  {0, 1, 0},
  {0, 0, 1},
  {0, 0, 0}
};

void setup(void) {
  Serial.begin(115200);

  pinMode(pin2, INPUT);
  attachInterrupt(0,WakeUp,LOW);

  lis.begin();
  lis.setRange(LIS3DH_RANGE_4_G);                 // 2, 4, 8 or 16 G!
  lis.setDataRate (LIS3DH_DATARATE_LOWPOWER_1K6HZ);  //POWERDOWN, 1_HZ, 10_HZ, 25_HZ, 50_HZ, 100_HZ 200_HZ, 400_HZ, LOWPOWER_1K6HZ, LOWPOWER_5KHZ
}

void loop() {
  count++;
  delay(1000);
  
  if (Serial.available()) {

    byte r = Serial.read();

    if (r == (byte)'s') {
      unsigned long startTime = micros();
      for (int i = 0; i < 1024; i++) {
        Elapsed.t_f = micros() - startTime;
        lis.read();
        x_acel.x_f = lis.x_g;
        y_acel.y_f = lis.y_g;
        z_acel.z_f = lis.z_g;
        calibration(x_acel.x_f, y_acel.y_f, z_acel.z_f);
        Serial.write(Elapsed.t_b, 4);
        Serial.write(x_acel.x_b, 4);
        Serial.write(y_acel.y_b, 4);
        Serial.write(z_acel.z_b, 4);
        delayMicroseconds(1640);
      }
    }
    count=0;
    delay(1000);
  }
  if (count>=10) {
    Serial.println("Entering Sleep");
    delay(100);
    count = 0;
    sleep();
  }
}

void calibration(float x_acel, float y_acel, float z_acel) {
  /* Calibrate Accelerometer to give true readings */
  float raw[4] = {x_acel, y_acel, z_acel, 1};
  float act_g[3];

  Matrix.Multiply((float*)raw, (float*)cal_mat, 1, 4, 3, (float*)act_g);

  x_acel = act_g[0];
  y_acel = act_g[1];
  z_acel = act_g[2];
}

void WakeUp(){
  //Null
}
void sleep() {
  /* Sleep mode to requde Power consumption
     Wake on pin 2 interrupt
  */

  set_sleep_mode(SLEEP_MODE_PWR_DOWN);
  sleep_enable();
  attachInterrupt(0,WakeUp,LOW);
  sleep_mode();

  sleep_disable();
  detachInterrupt(0);
  /* Note on wake from serial, first byte is not read */
}

