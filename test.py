import cv2
from line_follower import line_follower
from djitellopy import tello

capture = cv2.VideoCapture(0)

# me = tello.Tello()
# me.connect()
# me.takeoff()
# me.streamon()
# print(me.get_battery())

while True:
    _, frame = capture.read()
    # frame = me.get_frame_read().frame
    frame = cv2.resize(frame, (480, 360))

    line_follower(frame)

    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) == 27:
        # me.send_rc_control(0,0,0,0)
        # me.land()
        break

cv2.destroyAllWindows()