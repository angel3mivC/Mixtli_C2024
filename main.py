from flask import Flask, Response, jsonify
import cv2
from djitellopy import Tello

app = Flask(__name__)
me = Tello()
me.connect()
me.streamon()

def generate_frames():

    """ 
        Generates a stream of frames in order to capture them from the camera and display them as video
        Bits are coded as JPG for it to be frame by frame
    """

    while True:
        frame = me.get_frame_read().frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():

    """ 
        Frame update endpoint conection with the js in real time
    """

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/emergency_stop')
def emergency_stop():

    """ 
        Emergency stop method
    """
    
    me.emergency()
    return "Emergency stop executed"


@app.route('/land')
def land():
    """ 
        Landing method.
    """
    me.land()
    return "Drone landed"

@app.route('/start')
def start():
    """ 
    Drone initializing
    """
    me.takeoff()

    dron_height = me.get_height()

    if dron_height < 180:
        height = 110 - dron_height
        me.move_up(height)

    while True:
        """
        Follow detected line
        """
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
