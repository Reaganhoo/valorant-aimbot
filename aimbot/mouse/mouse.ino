#include <Mouse.h>

const int xAxis = A1;         // Analog sensor for X axis
const int yAxis = A2;         // Analog sensor for Y axis

int range = 12;               // Output range of X or Y movement
int responseDelay = 2;        // Response delay of the mouse, in ms
int threshold = range / 4;    // Resting threshold
int center = range / 2;       // Resting position value
int minima[] = {1023, 1023};  // Actual analogRead minima for (x, y)
int maxima[] = {0, 0};        // Actual analogRead maxima for (x, y)
int axis[] = {xAxis, yAxis};  // Pin numbers for (x, y)
int mouseReading[2];          // Final mouse readings for (x, y)

void setup() {
  // Initialize the Mouse library
  Mouse.begin();
}

void loop() {
  // Read and scale the two axes
  int xReading = readAxis(0);
  int yReading = readAxis(1);

  // Move the mouse
  //Mouse.move(xReading, yReading, 0);
  delay(responseDelay);
}

/*
  Reads an axis (0 or 1 for x or y) and scales the
  analog input range to a range from 0 to <range>
*/
int readAxis(int axisNumber) {
  int distance = 0; // Distance from center of the output range

  // Read the analog input
  int reading = analogRead(axis[axisNumber]);

  // Of the current reading exceeds the max or min for this axis, reset the max or min
  if (reading < minima[axisNumber]) {
    minima[axisNumber] = reading;
  }
  if (reading > maxima[axisNumber]) {
    maxima[axisNumber] = reading;
  }

  // Map the reading from the analog input range to the output range
  reading = map(reading, minima[axisNumber], maxima[axisNumber], 0, range);

  // If the output reading is outside from the rest position threshold,  use it
  if (abs(reading - center) > threshold) {
    distance = (reading - center);
  }

  // The Y axis needs to be inverted in order to map the movement correctly
  if (axisNumber == 1) {
    distance = -distance;
  }

  // Return the distance for this axis
  return distance;
}