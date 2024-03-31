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

capture = cv2.VideoCapture(0)

width = 480
senstivity = 3
fspeed = 15

vertex_x = np.empty(4, dtype=np.int16)
vertex_y = np.empty(4, dtype=np.int16)
aux = 0

font = cv2.FONT_HERSHEY_COMPLEX
kernel = np.ones((5,5), np.uint8)

while True:

    _, frame = capture.read()
    frame = cv2.resize(frame, (480, 360))


    l_h = cv2.getTrackbarPos("Low Hue", "Border detection") #Minimimum color range detected
    u_h = cv2.getTrackbarPos("Upper Hue", "Border detection") #Maximum color range detected
    l_s = cv2.getTrackbarPos("Low Saturation", "Border detection") #Minimimum saturation range detected
    u_s = cv2.getTrackbarPos("Upper Saturation", "Border detection") #Maximum saturation range detected
    l_v = cv2.getTrackbarPos("Low Value", "Border detection") #Minimimum color intensity detected
    u_v = cv2.getTrackbarPos("Upper Value", "Border detection") #Maximum color intensity detected


    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([l_h, l_s, l_v])
    upper = np.array([u_h, u_s, u_v])
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cntr in contours:
        area = cv2.contourArea(cntr)

        if area > 400:
            approx = cv2.approxPolyDP(cntr, 0.03*cv2.arcLength(cntr, True), True)
            cv2.drawContours(frame, [approx], 0, (0,0,0), 2)
            
            x = approx.ravel()[0]
            y = approx.ravel()[1]

            if len(approx) == 3:
                cv2.putText(frame, "Triangle", (x, y), font, 1, (0,0,0))
            elif len(approx) == 4:

                for i in range(4):
                    vertex_x[i] = approx[i][0][0]
                    vertex_y[i] = approx[i][0][1]

                for i in range(4):
                    for j in range(3):
                        if vertex_x[j] > vertex_x[j+1]:
                            aux = vertex_x[j+1]
                            vertex_x[j+1] = vertex_x[j]
                            vertex_x[j] = aux

                            aux = vertex_y[j+1]
                            vertex_y[j+1] = vertex_y[j]
                            vertex_y[j] = aux

                if vertex_y[0] > vertex_y[1]:
                    aux = vertex_y[1]
                    vertex_y[1] = vertex_y[0]
                    vertex_y[0] = aux

                if vertex_y[2] > vertex_y[3]:
                    aux = vertex_y[3]
                    vertex_y[3] = vertex_y[2]
                    vertex_y[2] = aux
                    
                upper_difference = abs(vertex_y[0] - vertex_y[2])
                lower_difference = abs(vertex_y[1] - vertex_y[3])

                if upper_difference < 50 and lower_difference < 50:
                    cv2.putText(frame, "Square", (x, y), font, 1, (0,0,0))
                else:
                    cv2.putText(frame, "Rhombus", (x, y), font, 1, (0,0,0))

            elif len(approx) == 5:
                cv2.putText(frame, "Pentagon", (x, y), font, 1, (0,0,0))
            elif len(approx) == 10:
                cv2.putText(frame, "Star", (x, y), font, 1, (0,0,0))
            elif len(approx) > 10:
                cv2.putText(frame, "Circle", (x, y), font, 1, (0,0,0))


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

    canvas = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)))
    cv2.imshow("Border detection", canvas)

    if cv2.waitKey(1) == 27: break

# me.land()

capture.release()
cv2.destroyAllWindows()