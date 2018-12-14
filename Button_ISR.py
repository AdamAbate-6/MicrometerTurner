import RPi.GPIO as GPIO
import Motor_Control1

class Button:

    def __init__(self, motorController):
        self.PIN = 24
        self.motorController = motorController
        GPIO.setup(self.PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
    def buttonISR(self, pin):
        print("Terminating program")
        self.motorController.setISR()
        print("If turn was interrupted, motor turned", self.motorController.getRelPosition(), "micrometers")