#Tips: It work only in python2

import time
import RPi.GPIO as GPIO
from bottle import request, Bottle, abort
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler


class Motor:
    def __init__(self,pinForward,pinBackward,pinPWM,frequency=500,speed=5):
        self.pinForward = pinForward
        self.pinBackward = pinBackward
        self.pinPWM = pinPWM
        self.speed = speed
        self.frequency = frequency

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinPWM,GPIO.OUT)
        self.p = GPIO.PWM(self.pinPWM,self.frequency)
        self.p.start(self.speed)
    def setDirection(self,direction):
        if direction == True:
            GPIO.output(self.pinForward, GPIO.HIGH)
            GPIO.output(self.pinBackward, GPIO.LOW)
        elif direction == False:
            GPIO.output(self.pinForward, GPIO.LOW)
            GPIO.output(self.pinBackward, GPIO.HIGH)
    def acc(self):
        self.speed += 5
        if self.speed >= 100:
            self.speed = 100
        self.p.ChangeDutyCycle(self.speed)
    def brake(self):
        self.speed = 0
        self.p.ChangeDutyCycle(self.speed)
    def clean_GPIO(self):
        self.p.stop()
        GPIO.cleanup()
        
app = Bottle()
@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    while True:
        try:
            message = wsock.receive()
            print(message)
            if(message=='accelerate'):
                motor.acc()
                print(motor.speed)
            if(message=='brake'):
                motor.brake()
            wsock.send('reset')
        except WebSocketError:
            break


GPIO.setwarnings(False)
motor = Motor(3,5,7,frequency=500,speed=50)



server = WSGIServer(("192.168.0.107", 8880), app, handler_class=WebSocketHandler)
server.serve_forever()



























