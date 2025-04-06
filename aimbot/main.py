import cv2
import numpy as np
import pydirectinput
import keyboard
import time
import mss  # Import mss for screenshots
import serial

ser = serial.Serial('COM11', 115200)

# Function to detect the target color and track the highest contour within a Y-axis range
def detect_target_color(frame, y_min, y_max):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color range for #FFFF93 detection
    #lower_bound = np.array([30, 150, 150])  # Lower bound for target color
    #upper_bound = np.array([30, 255, 255])  # Upper bound for target color (yellow)

    #lower_bound = np.array([140, 150, 100])  # Lower bound for target color 150
    #upper_bound = np.array([170, 255, 255])  # Upper bound for target color(purple)
    
    lower_bound = np.array([140, 120, 180])
    upper_bound = np.array([160, 200, 255])
    # Create a mask for the target color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    highest_y = float('inf')  # Initialize to a large value
    highest_contour_center = None  # To store the center of the highest contour

    for contour in contours:
        if cv2.contourArea(contour) > 0:  # Filter small contours
            # Calculate the moments of the contour
            M = cv2.moments(contour)
            if M["m00"] != 0:  # Avoid division by zero
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])
                height_offset = 2
                center_y -= height_offset

            else:
                continue  # Skip this contour if area is zero

            # Check if the contour's Y-coordinate is within the specified range
            if y_min <= center_y <= y_max:  # Use center_y for the check
                # Check if this contour is the highest one
                if center_y < highest_y:  # Compare y-coordinate
                    highest_y = center_y
                    highest_contour_center = (center_x, center_y)

    # If a highest contour was found, move the mouse to its center
    if highest_contour_center is not None:
        target_x = highest_contour_center[0]
        target_y = highest_contour_center[1]

        # Calculate the actual movement
        actual_movement_x = target_x - screen_center[0]
        actual_movement_y = target_y - screen_center[1]

        # Dynamic scaling based on distance
        distance = np.sqrt(actual_movement_x**2 + actual_movement_y**2)
        scale = min(50, max(1, distance / 22))  # Adjust scaling factor based on distance

        actual_movement_x *= scale
        actual_movement_y *= scale

        # Limit maximum movement to prevent vibrations
        max_movement_x = 128
        max_movement_y = 50
        actual_movement_x = np.clip(actual_movement_x, -max_movement_x, max_movement_x)
        actual_movement_y = np.clip(actual_movement_y, -max_movement_y, max_movement_y)

        # Send the movement command to Arduino
        message = f"{int(actual_movement_x)},{int(actual_movement_y)}\n"  # Format as "x,y\n"

        if -150 < actual_movement_x < 150 and -100 < actual_movement_y < 100:
            ser.write(message.encode('utf-8'))  # Encode the string to bytes and send
            print("actual_movement: ", actual_movement_x, actual_movement_y)
            print("Moving to target coordinates: ", target_x, target_y)

# Main loop
running = False  # Flag to control the tracking

# Define Y-axis range
y_min = 750  # Minimum Y-coordinate
y_max = 900  # Maximum Y-coordinate

# Screen Dimension
screen_width = 2560
screen_height = 1600
screen_center = (screen_width / 2, screen_height / 2)

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
    elif keyboard.is_pressed('k'):  # Press 'k' to quit
        print("Exiting...")
        break

    if running:
        # Capture screen using mss
        with mss.mss() as sct:
            screen = np.array(sct.grab(sct.monitors[1]))  # Grab the first monitor
            frame = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)  # Convert to BGR
            detect_target_color(frame, y_min, y_max)

# Clean up
ser.close()
cv2.destroyAllWindows()  # Close all OpenCV windows