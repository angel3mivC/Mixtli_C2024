from djitellopy import tello
from time import sleep
import cv2

me = tello.Tello()
me.connect()

print(me.get_battery())

#Basic movement
me.streamon()

me.takeoff()
me.send_rc_control()
me.send_rc_control(0, 5, 0, 0)
sleep(5)
me.send_rc_control(0, 0, 0, 0)

#Image Capture
print(me.stream_on)

while True:
    frame = me.get_frame_read().frame
    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) == 27:
        me.send_rc_control(0,0,0,0)
        me.land()
        break

cv2.destroyAllWindows()