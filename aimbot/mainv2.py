import cv2
import numpy as np
import keyboard
import time
import mss  # Import mss for screenshots
import serial
import threading
from config import Y_MIN, Y_MAX, SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_LOWER_BOUND, COLOR_UPPER_BOUND,SERIAL_PORT

# Initialize serial communication
ser = serial.Serial(SERIAL_PORT, 115200)

# Configuration Parameters
COLOR_LOWER_BOUND = np.array(COLOR_LOWER_BOUND)  # Lower bound for target color (HSV)
COLOR_UPPER_BOUND = np.array(COLOR_UPPER_BOUND)  # Upper bound for target color (HSV)

# Screen center
screen_center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

class ScreenCaptureThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.frame = None

    def run(self):
        with mss.mss() as sct:
            while self.running:
                self.frame = np.array(sct.grab(sct.monitors[1]))  # Grab the first monitor
                time.sleep(0.01)  # Sleep to reduce CPU usage

    def stop(self):
        self.running = False

def detect_target_color(frame, y_min, y_max):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, COLOR_LOWER_BOUND, COLOR_UPPER_BOUND)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    highest_y = float('inf')
    highest_contour_center = None

    for contour in contours:
        if cv2.contourArea(contour) > 0:
            M = cv2.moments(contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
            else:
                continue


            if y_min <= center_y <= y_max:
                if center_y < highest_y:
                    highest_y = center_y
                    highest_contour_center = (center_x, center_y)

    if highest_contour_center is not None:
        target_x = highest_contour_center[0]
        target_y = highest_contour_center[1]
        actual_movement_x = target_x - screen_center[0]
        actual_movement_y = target_y - screen_center[1]
        
        #distance = np.sqrt(actual_movement_x**2 + actual_movement_y**2)
        distance = np.sqrt(actual_movement_x**2)

        # Define parameters
        max_scale = 2.1#2.22#Scale when the target is very close
        min_scale = 1.52 # Scale when the target is at maximum distance

        max_distance = screen_center[0]  # Distance at which scale reaches min_scale

        # Calculate scaleX using the linear equation 
        scaleX = max_scale - ((max_scale - min_scale) / max_distance) * distance

        # Ensure scaleX does not go below min_scale
        scaleX = max(scaleX, min_scale)
        scaleY = 2

        actual_movement_x *= scaleX
        actual_movement_y *= scaleY
        return f"{int(actual_movement_x)},{int(actual_movement_y)}\n"
    return None

def main():
    screen_capture_thread = ScreenCaptureThread()
    screen_capture_thread.start()

    running = False  # Flag to control the tracking

    try:
        while True:
            # Check for keyboard input to start/stop tracking
            if keyboard.is_pressed('l'):  # Press 'l' to start
                running = True
                print("Started tracking target color.")
                time.sleep(0.5)  # Delay to prevent multiple triggers
                
            elif keyboard.is_pressed('p'):  # Press 'p' to pause
                running = False
                print("Paused tracking target color.")
                time.sleep(0.5)  # Delay to prevent multiple triggers

            elif keyboard.is_pressed('o'):  # Press 'p' to pause
                running = False
                test = f"{int(436)},{int(0)}\n"
                ser.write(test.encode('utf-8'))
                time.sleep(0.5)  # Delay to prevent multiple triggers

            elif keyboard.is_pressed('k'):  # Press 'k' to quit
                print("Exiting...")
                break

            if running and screen_capture_thread.frame is not None:
                message = detect_target_color(screen_capture_thread.frame, Y_MIN, Y_MAX)

                # Check for incoming serial data
                if ser.in_waiting > 0:  # If there is data waiting to be ready
                    serial_data = ser.readline().decode('utf-8').strip()  # Read a line from the serial port
                    if serial_data == "s":  # Check if the received data is "s"
                        print("receive")  # Print "receive" if the data is "s"
                        if message is not None:
                            # Move the mouse to the target position and click
                            ser.write(message.encode('utf-8'))  # Encode the string to bytes and send
                            ser.write(b'click\n')

                            print("Moving to target coordinates: ", message)

    finally:
        screen_capture_thread.stop()  # Stop the screen capture thread
        screen_capture_thread.join()  # Wait for the thread to finish
        ser.close()  # Close the serial connection
        cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()