from time import sleep
import RPi.GPIO as GPIO

class MotorControl:

    def __init__(self, mode, startingPosition=0):
        self.DIR = 20   # Direction GPIO Pin
        self.STEP = 21  # Step GPIO Pin
        self.CW = 1     # Clockwise Rotation
        self.CCW = 0    # Counterclockwise Rotation
        self.DPS = 1.8  # Number of degrees per step
        self.SPR = 360/self.DPS   # Steps per Revolution (360 / 1.8)

        self.mode = mode
        self.modeAdjust = 1
        self.delay = .0208
        self.positionChange = 0
        self.relPosition = startingPosition
        self.noISR = True

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.DIR, GPIO.OUT)
        GPIO.setup(self.STEP, GPIO.OUT)
        #Default to clockwise rotation
        GPIO.output(self.DIR, self.CW)

        MODE = (14, 15, 18)   # Microstep Resolution GPIO Pins
        GPIO.setup(MODE, GPIO.OUT)
        RESOLUTION = {'Full': (0, 0, 0),
                    'Half': (1, 0, 0),
                    '1/4': (0, 1, 0),
                    '1/8': (1, 1, 0),
                    '1/16': (0, 0, 1),
                    '1/32': (1, 0, 1)}
        GPIO.output(MODE, RESOLUTION[mode])
        self.adjustForMode()

        print("Motor controller initialized")
    
    def runMotor(self, degrees, direction):
        # Reset positionChange variable so that it can be adjusted in next turn
        self.positionChange = 0

        step_count = int(self.convertDegToStep(degrees))

        if(direction == "pos"):
            GPIO.output(self.DIR, self.CW)
            for x in range(step_count):
                if(self.noISR):
                    GPIO.output(self.STEP, GPIO.HIGH)
                    sleep(self.delay)
                    GPIO.output(self.STEP, GPIO.LOW)
                    sleep(self.delay)
                    #Calculate position after step
                    #Add to new position the number of degrees per step times the number of micrometers per degree
                    self.positionChange += self.modeAdjust*self.DPS*float(500)/float(360) 
                else:
                    break
                
            if(self.noISR):
                print("Turn executed")
            else:
                print("Turn interrupted\n")

        #sleep(.5)
        elif(direction == "neg"):
            GPIO.output(self.DIR, self.CCW)
            for x in range(step_count):
                if (self.noISR):
                    GPIO.output(self.STEP, GPIO.HIGH)
                    sleep(self.delay)
                    GPIO.output(self.STEP, GPIO.LOW)
                    sleep(self.delay)
                    self.positionChange -= self.modeAdjust*self.DPS*float(500)/float(360)
                else:
                    break
            
            if(self.noISR):
                print("Turn executed")
            else:
                print("Turn interrupted\n")
        
        else:
            print("Invalid direction given")
        
        self.relPosition += self.positionChange
        self.noISR = True

    def convertDegToStep(self, degrees):
        stepsPerDegree = self.SPR/float(360) #steps per rotation divided by degrees per rotation
        return degrees*stepsPerDegree
    
    def adjustForMode(self):
        if (self.mode == 'Half'):
            self.SPR *= 2
            self.delay /= 2
            self.modeAdjust = 0.5
        elif (self.mode == '1/4'):
            self.SPR *= 4
            self.delay /= 4
            self.modeAdjust = 0.25
        elif (self.mode == '1/8'):
            self.SPR *= 8
            self.delay /= 8
            self.modeAdjust = 1/float(8)
        elif (self.mode == '1/16'):
            self.SPR *= 16
            self.delay /= 16
            self.modeAdjust = 1/float(16)
        elif (self.mode == '1/32'):
            self.SPR *= 32
            self.delay /= 32
            self.modeAdjust = 1/float(32)
    
    def getPositionChange(self):
        return self.positionChange
    
    def getRelPosition(self):
        return self.relPosition
    
    def setISR(self):
        self.noISR = False
    
    def setRelPosition(self, position):
        self.relPosition = position


