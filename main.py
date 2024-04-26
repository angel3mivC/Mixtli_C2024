from djitellopy import Tello
import cv2
from shape_detection import shape_detection
import time

# Crear instancia del dron y conectarse
tello = Tello()
tello.connect()

time.sleep(2)
# Despegar
tello.takeoff()

# Iniciar el streaming de video
tello.streamon()

# Variable para controlar el bucle
keep_flying = True
# Variable para controlar las acciones del dron
movement_done = False

# Bucle principal para mostrar el video y controlar el dron
while keep_flying:
    # Obtener el frame actual
    frame = tello.get_frame_read().frame
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame = shape_detection(frame)
    cv2.imshow("Tello Camera", frame)
    # cv2.imshow("Shape detector", frame1)
    
    # Control del dron: Solo se ejecuta una vez
    if not movement_done:
        tello.move_forward(100)
        tello.rotate_counter_clockwise(90)
        tello.move_left(50)
        tello.land()  # Aterrizar
        movement_done = True
    
    # Esperar por una tecla para salir
    key = cv2.waitKey(1)  # Espera 1 ms para salir del bucle
    if key == 27:  # Salir si se presiona 'ESC'
        keep_flying = False

# Detener el streaming y cerrar ventanas
tello.streamoff()
cv2.destroyAllWindows()