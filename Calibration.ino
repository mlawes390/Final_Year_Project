/* Author: M.LAWES
    Curtin University of Technology
    Final Year Project 2016

    Accelerometer Calibration
*/

#include <Wire.h>
#include <SPI.h>
#include <Adafruit_LIS3DH.h>
#include <Adafruit_Sensor.h>
#include <MatrixMath.h>

#define LIS3DH_CS 10
// Hardware SPI
Adafruit_LIS3DH lis = Adafruit_LIS3DH(LIS3DH_CS);

byte null_;
int count = 500;
float x_sum;
float y_sum;
float z_sum;

float y[6][3] = {{0, 0, 1},
  {0, 0, -1},
  {0, 1, 0},
  {0, -1, 0},
  {1, 0, 0},
  { -1, 0, 0}
};

float w[6][4] = {{0, 0, 1, 1},
  {0, 0, -1, 1},
  {0, 1, 0, 1},
  {0, -1, 0, 1},
  {1, 0, 0, 1},
  { -1, 0, 0, 1}
};

float w_t[4][6];
float w_i[4][4];
float w_f[4][6];

float cal[4][3];

void setup() {
  Serial.begin(115200);

  lis.begin();
  lis.setRange(LIS3DH_RANGE_4_G);                 // 2, 4, 8 or 16 G!
  lis.setDataRate (LIS3DH_DATARATE_100_HZ);  //POWERDOWN, 1_HZ, 10_HZ, 25_HZ, 50_HZ, 100_HZ 200_HZ, 400_HZ, LOWPOWER_1K6HZ, LOWPOWER_5KHZ

  Serial.println("Calibration of LIS3DH Accelerometer Based Sensor Node");
  Serial.print("Range = "); Serial.print(2 << lis.getRange()); Serial.println("G");
}

void loop() {

  //Sample all 6 positions and obtain average
  Serial.println("Place accelerometer with Z axis upright");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[0][0], w[0][1], w[0][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);
    
  Serial.println("Place accelerometer with Z axis face down");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[1][0], w[1][1], w[1][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);

  Serial.println("Place accelerometer with Y axis upright");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[2][0], w[2][1], w[2][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);

  Serial.println("Place accelerometer with Y axis face down");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[3][0], w[3][1], w[3][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);

  Serial.println("Place accelerometer with X axis upright");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[4][0], w[4][1], w[4][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);

  Serial.println("Place accelerometer with X axis face down");
  Serial.println("Ready to Sample?");
  while (!Serial.available());
  sample(w[5][0], w[5][1], w[5][2]);
  while (Serial.available() > 0) {
    Serial.read();
  }
  delay(300);


  Serial.println("Calcuating");
  // Calculate calibration matrix
  Matrix.Transpose((float*)w, 6, 4, (float*)w_t);
  Matrix.Multiply((float*)w_t, (float*)w, 4, 6, 4, (float*)w_i);
  Matrix.Invert((float*)w_i, 4);
  Matrix.Multiply((float*)w_i, (float*)w_t, 4, 4, 6, (float*)w_f);
  Matrix.Multiply((float*)w_f, (float*)y, 4, 6, 3, (float*)cal);

  // Print Calibration Matrix
  Matrix.Print((float*)cal, 4, 3, "Calibration Matrix");

}

void sample(float &x_avg, float &y_avg, float &z_avg) {
  x_sum = 0;
  y_sum = 0;
  z_sum = 0;

  for (int i = 0; i < count; i++) {
    lis.read();
    x_sum += lis.x_g;
    y_sum += lis.y_g;
    z_sum += lis.z_g;
    delay(10);
  }
  x_avg = x_sum / count;
  y_avg = y_sum / count;
  z_avg = z_sum / count;
}
