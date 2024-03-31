from djitellopy import tello
import numpy as np
import cv2

def get_sensors(mask):
    imgs = np.hsplit(mask, 3)
    sensors = []
    for i, img in enumerate(imgs):
        pixelCount = cv2.countNonZero(img)
        #11520 representa en 20% del los pixeles de la imagen
        if pixelCount > 11520:
            sensors.append(1)
        else:
            sensors.append(0)
    return sensors

cv2.namedWindow("Border detection", cv2.WINDOW_AUTOSIZE)

cv2.createTrackbar("Low Hue", "Border detection", 0, 180, lambda x:None)
cv2.createTrackbar("Upper Hue", "Border detection", 180, 180, lambda x:None)
cv2.createTrackbar("Low Saturation", "Border detection", 0, 255, lambda x:None)
cv2.createTrackbar("Upper Saturation", "Border detection", 30, 255, lambda x:None)
cv2.createTrackbar("Low Value", "Border detection", 200, 255, lambda x:None)
cv2.createTrackbar("Upper Value", "Border detection", 255, 255, lambda x:None)

cv2.setWindowProperty("Border detection", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_FULLSCREEN)

# threshold = 0.2
# totalPixels = 57600
# sensors = np.array(3, dtype=bool)

# me = tello.Tello()
# me.connect()
# print(me.get_battery())
# me.streamon()

# me.takeoff()

capture = cv2.VideoCapture(0)

width = 480
senstivity = 3
fspeed = 15

while True:
    l_h = cv2.getTrackbarPos("Low Hue", "Border detection") #Minimimum color range detected
    u_h = cv2.getTrackbarPos("Upper Hue", "Border detection") #Maximum color range detected
    l_s = cv2.getTrackbarPos("Low Saturation", "Border detection") #Minimimum saturation range detected
    u_s = cv2.getTrackbarPos("Upper Saturation", "Border detection") #Maximum saturation range detected
    l_v = cv2.getTrackbarPos("Low Value", "Border detection") #Minimimum color intensity detected
    u_v = cv2.getTrackbarPos("Upper Value", "Border detection") #Maximum color intensity detected

    _, frame = capture.read()
    # frame = me.get_frame_read().frame
    # frame = cv2.flip(frame, 0)
    frame = cv2.resize(frame, (480, 360))

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame, contours, -1, (255,0,0), 2)

    if contours:
        biggest = max(contours, key = cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w//2
        cy = y + h//2

        cv2.circle(frame, (cx, cy), 10, (255,0,0), cv2.FILLED)

    sensors = get_sensors(mask)

    #Envio de comandos

    #Translation
    lr = cx - width//2
    lr = int(np.clip(lr, -10, 10))
    if lr < 2 and lr > -2: lr = 0

    #Rotation

    if sensors == [1, 0, 0]: curve = -25
    elif sensors == [1, 1, 0]: curve = -15
    elif sensors == [0, 1, 0]: curve = 0
    elif sensors == [0, 1, 1]: curve = 15
    elif sensors == [0, 0, 1]: curve = 25
    elif sensors == [0, 0, 0]: curve = 0
    elif sensors == [1, 1, 1]: curve = 0
    elif sensors == [1, 0, 1]: curve = 0

    # me.send_rc_control(lr, fspeed, 0, curve)

    canvas = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
    cv2.imshow("Border detection", canvas)
    # cv2.imshow("Frame", frame)
    # cv2.imshow("Filter", mask)

    if cv2.waitKey(1) == 27: break

# me.land()

capture.release()
cv2.destroyAllWindows()