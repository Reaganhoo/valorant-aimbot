"""import cv2
import numpy as np
import keyboard
import time
import mss  # Import mss for screenshots

# Function to detect the target color and track the highest contour within a Y-axis range
def detect_target_color(frame, y_min, y_max):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color range for detection
    #lower_bound = np.array([30, 150, 100])  # Lower bound for target color 150
    #upper_bound = np.array([30, 255, 255])  # Upper bound for target color (yellow protanopia)

    #lower_bound = np.array([140,111,100])  # Lower bound for target color 150
    #upper_bound = np.array([148,154,194])  # Upper bound for target color(purple)

    lower_bound = np.array([140, 150, 100])  # Lower bound for target color 150
    upper_bound = np.array([170, 255, 255])  # Upper bound for target color(purple)
    
    # Create a mask for the target color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Create a mask to highlight the specific Y-coordinate range
    height, width = mask.shape
    y_range_mask = np.zeros_like(mask)  # Create a mask of the same size as the original mask
    y_range_mask[y_min:y_max, :] = 255  # Set the specified Y-coordinate range to white

    # Combine the original mask with the Y-coordinate range mask
    combined_mask = cv2.bitwise_and(mask, y_range_mask)

    # Resize the combined mask to a smaller size (1:8 ratio)
    combined_mask_resized = cv2.resize(combined_mask, (width // 4, height // 4))

    # Display the resized combined mask
    cv2.imshow("Mask with Y-Coordinate Range", combined_mask_resized)  # Show the mask
    cv2.waitKey(1)

# Main loop
running = False  # Flag to control the tracking

# Define Y-axis range
y_min = 750  # Minimum Y-coordinate
y_max = 900  # Maximum Y-coordinate

while True:
    # Check for keyboard input to start/stop tracking
    if keyboard.is_pressed('s'):  # Press 's' to start
        running = True
        print("Started tracking target color.")
        time.sleep(0.5)  # Delay to prevent multiple triggers
    elif keyboard.is_pressed('p'):  # Press 'p' to pause
        running = False
        print("Paused tracking target color.")
        time.sleep(0.5)  # Delay to prevent multiple triggers
    elif keyboard.is_pressed('q'):  # Press 'q' to quit
        print("Exiting...")
        break

    if running:
        # Capture screen using mss
        with mss.mss() as sct:
            screen = np.array(sct.grab(sct.monitors[1]))  # Grab the first monitor
            frame = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)  # Convert to BGR
            detect_target_color(frame, y_min, y_max)

# Clean up
cv2.destroyAllWindows()  # Close all OpenCV windows"""

import cv2
import numpy as np
import keyboard
import time
import mss  # Import mss for screenshots

# Function to detect the target color and track the highest contour within a Y-axis range
def detect_target_color(frame, y_min, y_max):
    # Convert frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define color range for detection
    #lower_bound = np.array([140, 150, 100])  # Lower bound for target color (purple)
    #upper_bound = np.array([170, 255, 255])  # Upper bound for target color (purple)

    lower_bound = np.array([140, 120, 180])  # Lower bound for target color (new purple)
    upper_bound = np.array([160, 200, 255]) 
    
    # Create a mask for the target color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Create a mask to highlight the specific Y-coordinate range
    height, width = mask.shape
    y_range_mask = np.zeros_like(mask)  # Create a mask of the same size as the original mask
    y_range_mask[y_min:y_max, :] = 255  # Set the specified Y-coordinate range to white

    # Combine the original mask with the Y-coordinate range mask
    combined_mask = cv2.bitwise_and(mask, y_range_mask)

    # Find contours in the combined mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)#cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variable to track the highest y-coordinate
    highest_y = float('inf')  # Start with a large value
    highest_contour = None  # To store the highest contour

    # Iterate through contours to find the highest one
    for contour in contours:
        if cv2.contourArea(contour) > 0:  # Filter out small contours
            x, y, w, h = cv2.boundingRect(contour)  # Get the bounding rectangle
            
            # Check if this contour's y-coordinate is the highest (smallest y value)
            if y < highest_y:
                highest_y = y
                highest_contour = contour  # Store the highest contour

    # If a highest contour was found, draw a rectangle around it
    if highest_contour is not None:
        x, y, w, h = cv2.boundingRect(highest_contour)  # Get the bounding rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Draw rectangle on the frame
        print(f"Highest Y-coordinate of the target: {y}")  # Print the highest y-coordinate

    # Resize the combined mask to a smaller size (1:8 ratio)
    combined_mask_resized = cv2.resize(combined_mask, (width // 4, height // 4))

    # Display the resized combined mask
    cv2.imshow("Mask with Y-Coordinate Range", combined_mask_resized)  # Show the mask
    cv2.waitKey(1)

# Main loop
running = False  # Flag to control the tracking

# Define Y-axis range
y_min = 750  # Minimum Y-coordinate
y_max = 900  # Maximum Y-coordinate

while True:
    # Check for keyboard input to start/stop tracking
    if keyboard.is_pressed('s'):  # Press 's' to start
        running = True
        print("Started tracking target color.")
        time.sleep(0.5)  # Delay to prevent multiple triggers
    elif keyboard.is_pressed('p'):  # Press 'p' to pause
        running = False
        print("Paused tracking target color.")
        time.sleep(0.5)  # Delay to prevent multiple triggers
    elif keyboard.is_pressed('q'):  # Press 'q' to quit
        print("Exiting...")
        break

    if running:
        # Capture screen using mss
        with mss.mss() as sct:
            screen = np.array(sct.grab(sct.monitors[1]))  # Grab the first monitor
            frame = cv2.cvtColor(screen, cv2.COLOR_BGRA2BGR)  # Convert to BGR
            detect_target_color(frame, y_min, y_max)

# Clean up
cv2.destroyAllWindows()  # Close all OpenCV windows