import cv2
import numpy as np

cv2.namedWindow("HSV Configuration")
cv2.createTrackbar("L-H", "HSV Configuration", 0, 255, lambda x:None)
cv2.createTrackbar("L-S", "HSV Configuration", 121, 255, lambda x:None)
cv2.createTrackbar("L-V", "HSV Configuration", 109, 255, lambda x:None)
cv2.createTrackbar("U-H", "HSV Configuration", 255, 255, lambda x:None)
cv2.createTrackbar("U-S", "HSV Configuration", 255, 255, lambda x:None)
cv2.createTrackbar("U-V", "HSV Configuration", 243, 255, lambda x:None)

capture = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_COMPLEX
kernel = np.ones((5,5), np.uint8)

l_h = cv2.getTrackbarPos("L-H", "HSV Configuration")
l_s = cv2.getTrackbarPos("L-S", "HSV Configuration")
l_v = cv2.getTrackbarPos("L-V", "HSV Configuration")
u_h = cv2.getTrackbarPos("U-H", "HSV Configuration")
u_s = cv2.getTrackbarPos("U-S", "HSV Configuration")
u_v = cv2.getTrackbarPos("U-V", "HSV Configuration")

lower_red = np.array([l_h, l_s, l_v])
upper_red = np.array([u_h, u_s, u_v])

vertex_x = np.empty(4, dtype=np.int16)
vertex_y = np.empty(4, dtype=np.int16)
aux = 0

while True:
    _, frame = capture.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_red, upper_red)
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

    cv2.imshow("Capture", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) == 27: break

capture.release()
cv2.destroyAllWindows()