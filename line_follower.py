import numpy as np
import cv2

cv2.namedWindow("Line")
cv2.createTrackbar("L-H", "Line", 0, 180, lambda x:None)
cv2.createTrackbar("L-S", "Line", 0, 255, lambda x:None)
cv2.createTrackbar("L-V", "Line", 135, 255, lambda x:None)
cv2.createTrackbar("U-H", "Line", 180, 180, lambda x:None)
cv2.createTrackbar("U-S", "Line", 25, 255, lambda x:None)
cv2.createTrackbar("U-V", "Line", 255, 255, lambda x:None)

def get_sensors(mask):
    imgs = np.hsplit(mask, 3)
    sensors = []
    for i, img in enumerate(imgs):
        pixelCount = cv2.countNonZero(img)
        if pixelCount > 11520:  #11520 representa en 20% del los pixeles de la imagen
            sensors.append(1)
        else:
            sensors.append(0)
    return sensors

def line_follower(frame):

    l_h = cv2.getTrackbarPos("L-H", "Line")
    l_s = cv2.getTrackbarPos("L-S", "Line")
    l_v = cv2.getTrackbarPos("L-V", "Line")
    u_h = cv2.getTrackbarPos("U-H", "Line")
    u_s = cv2.getTrackbarPos("U-S", "Line")
    u_v = cv2.getTrackbarPos("U-V", "Line")

    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])

    # hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    contours, _ =cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # cv2.imshow("Mask", mask)

    if contours:
        biggest = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(biggest)
        cx = x + w//2
        cy = y + h//2

        cv2.drawContours(frame, contours, -1, (255,0,0), 5)
        cv2.circle(frame, (cx, cy), 10, (255,0,0), cv2.FILLED)

    sensors = get_sensors(mask)
    # print(sensors)




##Envio de comandos

# #Translation
# lr = cx - 240 #width/2
# lr = int(np.clip(lr, -10, 10))
# if lr < 2 and lr > -2: lr = 0

##Rotation

# if sensors == [1, 0, 0]: yaw = -25
# elif sensors == [1, 1, 0]: yaw = -15
# elif sensors == [0, 1, 0]: yaw = 0
# elif sensors == [0, 1, 1]: yaw = 15
# elif sensors == [0, 0, 1]: yaw = 25
# elif sensors == [0, 0, 0]: yaw = 0
# elif sensors == [1, 1, 1]: yaw = 0
# elif sensors == [1, 0, 1]: yaw = 0

# me.send_rc_control(lr, fspeed, 0, yaw)