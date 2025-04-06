// USB
#include <usbhub.h>
USB Usb;
USBHub Hub(&Usb);

// Human Interface Device
#include <hidboot.h>
HIDBoot<USB_HID_PROTOCOL_MOUSE> HidMouse(&Usb);

// Mouse Control
#include <Mouse.h>


bool ignore = false;

// ----- Mouse Report Parser
class MouseRptParser : public MouseReportParser
{
  protected:
    void OnMouseMove(MOUSEINFO *mi);
    void OnLeftButtonUp(MOUSEINFO *mi);
    void OnLeftButtonDown(MOUSEINFO *mi);
    void OnRightButtonUp(MOUSEINFO *mi);
    void OnRightButtonDown(MOUSEINFO *mi);
    void OnMiddleButtonUp(MOUSEINFO *mi);
    void OnMiddleButtonDown(MOUSEINFO *mi);
};

void MouseRptParser::OnMouseMove(MOUSEINFO *mi)
{
    // Get the change in mouse position
    int dx = mi->dX;
    int dy = mi->dY;

    // Move the cursor using Mouse.h

    Mouse.move(dx, dy);
}

void MouseRptParser::OnLeftButtonUp(MOUSEINFO *mi) { Mouse.release(MOUSE_LEFT); }
void MouseRptParser::OnLeftButtonDown(MOUSEINFO *mi) {Mouse.press(MOUSE_LEFT);}
void MouseRptParser::OnRightButtonUp(MOUSEINFO *mi) {}
void MouseRptParser::OnRightButtonDown(MOUSEINFO *mi) {Mouse.click(MOUSE_RIGHT);}
void MouseRptParser::OnMiddleButtonUp(MOUSEINFO *mi) {}
void MouseRptParser::OnMiddleButtonDown(MOUSEINFO *mi) {Serial.println("s");}

MouseRptParser Prs;

// -----------------
//  setup()
// -----------------
void setup()
{
    // Serial port
    Serial.begin(115200);
    pinMode(13, OUTPUT);

    // Initialize USB card
    Usb.Init();
    HidMouse.SetReportParser(0, &Prs);

    // Initialize mouse control
    Mouse.begin();

    Serial.println("Mouse Ready");
}

// -----------------
//  loop()
// -----------------
void loop()
{
    Usb.Task();
    // Check for serial input
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n'); // Read until newline

        // Parse the coordinates
        int commaIndex = input.indexOf(',');
        if (commaIndex > 0) {
            String xStr = input.substring(0, commaIndex); // Get the X coordinate
            String yStr = input.substring(commaIndex + 1); // Get the Y coordinate

           // Convert to integers
            int targetX = xStr.toInt();
            int targetY = yStr.toInt();
            int currentX = 0;
            int currentY = 0;

            // Move the mouse incrementally
            while (currentX != targetX || currentY != targetY) {
                int deltaX = targetX - currentX;
                int deltaY = targetY - currentY;

                // Calculate the movementk
                int moveX = constrain(deltaX, -127, 127); // Limit movement to max 128
                int moveY = constrain(deltaY, -127, 127);   // Limit movement to max 50

                // Move the mouse
                Mouse.move(moveX, moveY);
                Serial.println(moveX);
                currentX += moveX; // Update current X position
                currentY += moveY; // Update current Y position

                //delay(1000); // Small delay to allow for smooth movement
            }
            Mouse.click(MOUSE_LEFT); // Perform a left mouse click
        } /*else if (input.equals("click")) { // Check for the click command
            Mouse.click(MOUSE_LEFT); // Perform a left mouse click
        }*/
    } 
}