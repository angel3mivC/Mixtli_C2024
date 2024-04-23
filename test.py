import cv2
from djitellopy import tello
from shape_detection import shape_detection
#from line_follower import line_detection

#me = tello.Tello()
#me.connect()
#print(me.get_battery)
#me.streamon()

capture = cv2.VideoCapture(0)

while True:

    #frame = me.get_frame_read().frame
    _, frame = capture.read()

    frame = shape_detection(frame)

    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) == 27:
        #me.send_rc_control(0,0,0,0)
        #me.land()
        break

capture.release()
cv2.destroyAllWindows()