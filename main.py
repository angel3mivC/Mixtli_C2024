import cv2
from djitellopy import tello
from shape_detection import shape_detection
from collections import Counter

# me = tello.Tello()
# me.connect()
# me.takeoff()
# me.streamon()
# print(me.get_battery())

capture = cv2.VideoCapture(0)
detected_shapes = 0
shapes = []

while True:
    _, frame = capture.read()
    # frame = me.get_frame_read().frame
    frame = cv2.resize(frame, (480, 360))
    
    shape = shape_detection(frame)
    shapes.append(shape)
    detected_shapes += 1

    if detected_shapes == 30:
        count = Counter(shapes)
        most_common_shape = max(count, key=count.get)

        # print(most_common_shape)

        # if most_common_shape == "square":
            # me.rotate_clockwise(270)
            # me.rotate_clockwise(-90)
        # elif most_common_shape == "pentagon":
            # me.rotate_clockwise(90)
        #elif most_common_shape == "circle":
            # me.move_forward(20)

        shapes = []
        detected_shapes = 0

    cv2.imshow("Capture", frame)

    if cv2.waitKey(1) == 27:
        # me.send_rc_control(0,0,0,0)
        # me.land()
        break

cv2.destroyAllWindows()