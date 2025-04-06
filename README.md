# Aimbot with OpenCV and Arduino Leonardo

This project implements an aimbot using OpenCV in Python, which detects a specific color on the screen and calculates the necessary mouse movements to aim at it. The application communicates with an Arduino Leonardo equipped with a USB shield to control the mouse cursor.

## Features

- Real-time color detection using OpenCV.
- Adjustable tracking parameters through a configuration file.
- Serial communication with an Arduino Leonardo for mouse control.
- Simple keyboard controls to start, pause, and stop tracking.

## Prerequisites

- Python 3.x
- Required libraries:
  - OpenCV
  - NumPy
  - Keyboard
  - MSS
  - PySerial

You can install the required libraries using the following command:

```bash
pip install -r requirements.txt
```

## config.py
  The configuration parameters are defined in the config.py file. You can adjust the following settings:
  
  SERIAL_PORT: The COM port to which your Arduino Leonardo is connected (e.g., 'COM11').
  Y_MIN: Minimum Y-coordinate for tracking.
  Y_MAX: Maximum Y-coordinate for tracking.
  SCREEN_WIDTH: Width of the screen in pixels.
  SCREEN_HEIGHT: Height of the screen in pixels.
  COLOR_LOWER_BOUND: Lower bound for the target color in HSV format.
  COLOR_UPPER_BOUND: Upper bound for the target color in HSV format.

## HSV_test.py

  Purpose: Detects a specific shade of purple on the screen within a defined Y-axis range using OpenCV and mss.
  
  Libraries Used:
  
  cv2: For image processing.
  numpy: For numerical operations and array handling.
  keyboard: To detect keyboard inputs.
  time: For time-related functions.
  mss: For capturing screenshots.
  Functionality:
  
  Converts captured frames from BGR to HSV color space for better color detection.
  Defines a color range for detecting purple.
  Creates a mask to isolate the target color within specified Y-coordinate limits.
  Finds contours in the masked image and identifies the highest contour based on the Y-coordinate.
  Draws a rectangle around the highest contour and prints its Y-coordinate.
  User Controls:
  
  Press 's' to start tracking the target color.
  Press 'p' to pause tracking.
  Press 'q' to quit the program.
  Display: Shows a resized mask of the detected color and the bounding box around the highest contour in a window.
  
  Execution: Continuously runs until the user decides to exit, providing real-time tracking of the specified color.

## main.py

  Purpose: Detects a specific shade of purple on the screen and sends movement commands to an Arduino based on the detected position of the color.
  
  Libraries Used:
  
  cv2: For image processing.
  numpy: For numerical operations and array handling.
  pydirectinput: For simulating mouse movements (not used in the provided code).
  keyboard: To detect keyboard inputs.
  time: For time-related functions.
  mss: For capturing screenshots.
  serial: For serial communication with Arduino.
  Serial Communication:
  
  Initializes a serial connection to an Arduino on COM11 at a baud rate of 115200.
  Function: detect_target_color(frame, y_min, y_max):
  
  Converts the captured frame from BGR to HSV color space for better color detection.
  Defines a color range for detecting a specific shade of purple.
  Creates a mask to isolate the target color.
  Finds contours in the masked image and calculates the center of each contour.
  Filters contours based on area and checks if their Y-coordinate (center) is within the specified range.
  Identifies the highest contour and calculates the movement needed to center the mouse on it.
  Movement Calculation:
  
  Computes the actual movement required based on the distance from the screen center.
  Applies dynamic scaling to the movement based on distance to prevent excessive movement.
  Limits maximum movement to avoid vibrations.
  Formats the movement as a string and sends it to the Arduino if within specified limits.
  User Controls:
  
  Press 'l' to start tracking the target color.
  Press 'p' to pause tracking.
  Press 'k' to quit the program.
  Main Loop:
  
  Continuously captures the screen and processes frames to detect the target color while tracking is active.
  Cleanup:
  
  Closes the serial connection and all OpenCV windows upon exiting the program.

## main2.py

  Purpose: Detects a specific color on the screen and sends movement commands to an Arduino based on the detected position, while also allowing for manual control via keyboard inputs.
  
  Libraries Used:
  
  cv2: For image processing.
  numpy: For numerical operations and array handling.
  keyboard: To detect keyboard inputs.
  time: For time-related functions.
  mss: For capturing screenshots.
  serial: For serial communication with Arduino.
  threading: To handle screen capture in a separate thread.
  config: Imports configuration parameters for color detection and screen dimensions.
  Serial Communication:
  
  Initializes a serial connection to an Arduino using a port defined in the configuration.
  Configuration Parameters:
  
  Sets lower and upper bounds for the target color in HSV format, as well as screen dimensions and Y-coordinate limits.
  Class: ScreenCaptureThread:
  
  Inherits from threading.Thread to capture the screen in a separate thread.
  Continuously grabs frames from the screen while the thread is running, with a short sleep to reduce CPU usage.
  Provides a method to stop the thread.
  Function: detect_target_color(frame, y_min, y_max):
  
  Converts the captured frame from BGR to HSV color space.
  Creates a mask to isolate the target color based on the defined color bounds.
  Finds contours in the masked image and calculates the center of each contour.
  Identifies the highest contour within the specified Y-coordinate range.
  Calculates the movement needed to center the mouse on the detected color, applying dynamic scaling based on distance.
  Main Functionality:
  
  Starts the screen capture thread.
  Continuously checks for keyboard inputs to control tracking:
  Press 'l' to start tracking.
  Press 'p' to pause tracking.
  Press 'o' to send a predefined command to the Arduino.
  Press 'k' to quit the program.
  If tracking is active, processes the captured frame to detect the target color and sends movement commands to the Arduino if a specific signal is received.
  Serial Data Handling:
  
  Checks for incoming serial data from the Arduino and responds to specific commands (e.g., "s") to trigger mouse movement and clicking.
  Cleanup:
  
  Stops the screen capture thread, closes the serial connection, and destroys all OpenCV windows upon exiting the program.
  Execution: The main() function is called when the script is run, initiating the entire process.
