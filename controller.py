from djitellopy import tello
import cv2
import numpy as np

# me = tello.Tello()
# me.connect()
# me.takeoff()
# me.streamon()
# print(me.get_battery())

cv2.namedWindow("HSV Configuration")
cv2.createTrackbar("L-H", "HSV Configuration", 0, 179, lambda x:None)
cv2.createTrackbar("L-S", "HSV Configuration", 121, 255, lambda x:None)
cv2.createTrackbar("L-V", "HSV Configuration", 109, 255, lambda x:None)
cv2.createTrackbar("U-H", "HSV Configuration", 22, 179, lambda x:None)
cv2.createTrackbar("U-S", "HSV Configuration", 255, 255, lambda x:None)
cv2.createTrackbar("U-V", "HSV Configuration", 243, 255, lambda x:None)

capture = cv2.VideoCapture(0)

while True:

    l_h = cv2.getTrackbarPos("L-H", "HSV Configuration")
    l_s = cv2.getTrackbarPos("L-S", "HSV Configuration")
    l_v = cv2.getTrackbarPos("L-V", "HSV Configuration")
    u_h = cv2.getTrackbarPos("U-H", "HSV Configuration")
    u_s = cv2.getTrackbarPos("U-S", "HSV Configuration")
    u_v = cv2.getTrackbarPos("U-V", "HSV Configuration")

    # frame = me.get_frame_read().frame

    _, frame = capture.read()
    
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(frame, lower, upper)

    # foreward = 0
    # side = 0
    # yaw = 0

    # if cv2.waitKey() == ord("w"):
    #     foreward = 50
    # if cv2.waitKey() == ord("s"):
    #     foreward = -50
    # if cv2.waitKey() == ord("d"):
    #     side = 50
    # if cv2.waitKey() == ord("a"):
    #     side = -50
    # if cv2.waitKey() == ord("q"):
    #     yaw = -50
    # if cv2.waitKey() == ord("e"):
    #     yaw = 50
    
    # me.send_rc_control(side,foreward,0,yaw)

    cv2.imshow("Capture", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == 27:
        # me.send_rc_control(0,0,0,0)
        # me.land()
        break

cv2.destroyAllWindows()