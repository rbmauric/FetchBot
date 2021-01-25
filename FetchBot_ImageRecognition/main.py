# Team F: FetchBot
# Image Recognition and Tracking
# Ryan Mauricio
# 10/13/20

# Import Libraries
import cv2
import servo
import numpy as np


# Dummy Callback Function
def nothing(x):
    pass


# Windows and Trackbars for Hue, Saturation, and Value
# cv2.namedWindow("Tracking")
# cv2.createTrackbar("LH", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("LS", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("LV", "Tracking", 0, 255, nothing)
# cv2.createTrackbar("UH", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("US", "Tracking", 255, 255, nothing)
# cv2.createTrackbar("UV", "Tracking", 255, 255, nothing)

# Start Video Capture and Check If Valid
cap = cv2.VideoCapture(0)
servo.ServoInit()

print(cap.isOpened())

# Infinite Loop to Read All Frames
while True:

    # Capture Each Frame
    _, frame = cap.read()
    # frame = cv2.imread('smarties.png') # Testing HSV Tracking

    # Convert Image to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Lower and Upper HSV
    l_h = cv2.getTrackbarPos("LH", "Tracking")
    l_s = cv2.getTrackbarPos("LS", "Tracking")
    l_v = cv2.getTrackbarPos("LV", "Tracking")

    u_h = cv2.getTrackbarPos("UH", "Tracking")
    u_s = cv2.getTrackbarPos("US", "Tracking")
    u_v = cv2.getTrackbarPos("UV", "Tracking")

    # l_hsv = np.array([l_h, l_s, l_v])
    # u_hsv = np.array([u_h, u_s, u_v])

    l_hsv = np.array([28, 104, 67])
    u_hsv = np.array([62, 255, 255])

    # Mask Original Image
    mask = cv2.inRange(hsv, l_hsv, u_hsv)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    # Contours
    ret, thresh = cv2.threshold(mask, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
    area = 0
    angle = 90

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        print('area:', area)

        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        x_mid = int((x + x + w) / 2)
        x_ref = x_mid - 320
        angle = int(x_mid / 3.5556)
        break;

    if area > 1000:
        cv2.line(frame, (x_mid, 0), (x_mid, 480), (255, 0, 0), 2)
        servo.SetAngle(angle)
    else:
        cv2.line(frame, (320, 0), (320, 480), (255, 0, 0), 2)
        x_ref = 0

    print('x_ref:', x_ref)
    print('angle:', angle)

    # Show Original Image (Flipped), Mask, and Result
    flip = cv2.flip(frame, -1)
    flip2 = cv2.flip(res, -1)
    cv2.imshow("frame", flip)
    # cv2.imshow("mask", mask)
    # cv2.imshow("res", flip2)

    # If Escape Key is Pressed, Exit
    if cv2.waitKey(1) == 27:
        servo.CleanUp()
        break

# Stop Capturing Video
cap.release()
cv2.destroyAllWindows()

