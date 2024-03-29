from djitellopy import tello
import numpy as np
import cv2

def nothing(): pass

cv2.namedWindow("Line")
cv2.createTrackbar("L-H", "Line", 0, 180, nothing)
cv2.createTrackbar("L-S", "Line", 121, 255, nothing)
cv2.createTrackbar("L-V", "Line", 109, 255, nothing)
cv2.createTrackbar("U-H", "Line", 180, 180, nothing)
cv2.createTrackbar("U-S", "Line", 255, 255, nothing)
cv2.createTrackbar("U-V", "Line", 243, 255, nothing)

capture = cv2.VideoCapture(0)

while True:
    frame = capture.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h = cv2.getTrackbarPos("L-H", "HSV Configuration")
    l_s = cv2.getTrackbarPos("L-S", "HSV Configuration")
    l_v = cv2.getTrackbarPos("L-V", "HSV Configuration")
    u_h = cv2.getTrackbarPos("U-H", "HSV Configuration")
    u_s = cv2.getTrackbarPos("U-S", "HSV Configuration")
    u_v = cv2.getTrackbarPos("U-V", "HSV Configuration")

    lower_red = np.array([l_h, l_s, l_v])
    upper_red = np.array([u_h, u_s, u_v])

    mask = cv2.inRange(hsv, lower_red, upper_red)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key = cv2.contourArea())

    x, y, w, h = cv2.boundingRect(biggest)
    cx = x + w//2
    cy = y + h//2

    cv2.drawContours(frame, contours, -1, (0,0,255), 7)
    cv2.circle(frame, (cx, cy), 10, (0,0,255), cv2.FILLED)

    


    if cv2.waitKey(1) == 27: break

capture.release()
cv2.destroyAllWindows()