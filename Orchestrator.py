import Motor_Control1
import Button_ISR
import Torque_ISR
import RPi.GPIO as GPIO
from time import sleep
import random
#import smbus 

class Orchestrator:

    def __init__(self, motorController):
        self.motorController = motorController  
        self.button = Button_ISR.Button(self.motorController)
        #self.adc = Torque_ISR.ADC(self.motorController)
        GPIO.setmode(GPIO.BCM)

        GPIO.add_event_detect(self.button.PIN, GPIO.RISING, callback=self.button.buttonISR, bouncetime=2000)
        #GPIO.add_event_detect(self.adc.PIN, GPIO.RISING, callback=self.adc.torqueISR, bouncetime=1000)

        print("Orchestrator initialized")

    def requestTurn(self):
        mm = int(input("Please enter an integer number of micrometers to turn: "))
        degrees = 360/float(500)*mm

        direction = input("Please enter direction in which to turn (pos or neg): ")
        if (direction != "pos" and direction != "neg"):
            direction = input("Please enter a valid direction (pos or neg): ")

        return [degrees,direction]
    
    def turnMotor(self, degrees, direction):
        #print("Turning motor", degrees, "degrees in", direction, "direction")
        self.motorController.runMotor(degrees, direction)
        print("Turned motor",self.motorController.getPositionChange(),"micrometers")
        print("New position is",self.motorController.getRelPosition(),"micrometers\n")
    
    def execute(self):
        while (True):
            multTurns = input("Would you like to make multiple turns at once? (Y/N) ")
            if (multTurns == "Y"):
                multTurnsArr = []
                anotherTurn = True
                print("First turn:")
                while(anotherTurn):
                    #print("Please enter a turn")
                    #mm = input("How many micrometers? ")
                    #direction = input("In what direction? ")
                    #turnArr = [mm, direction]
                    multTurnsArr.append(self.requestTurn())

                    oneMore = input("Enter another turn? (Y/N) ")
                    print('\n')
                    if(oneMore == 'N'):
                        anotherTurn = False
                    
                for i in range(0, len(multTurnsArr)):
                    self.turnMotor(multTurnsArr[i][0], multTurnsArr[i][1])
                    if(i != len(multTurnsArr) - 1):
                        input("Press any key for next turn")

            else:
                turn = self.requestTurn()
                self.turnMotor(turn[0], turn[1])
            
            adjMode = input("Would you like to adjust the resolution? (Y/N) ")
            if (adjMode == 'Y'):
                self.adjustMode()

        
        GPIO.cleanup()
    
    def adjustMode(self):
        startingPosition = self.motorController.getRelPosition()
        newMode = input("What should the new mode be? \n(Options: Full, Half, 1/4, 1/8, 1/16, 1/32) ")
        self.motorController = Motor_Control1.MotorControl(newMode, startingPosition)
    
if __name__ == '__main__':
    print("__________________________________________________\n")
    print("MICROMETER McTURNFACE MK 1.1\n")
    print("Copyright 2018, Cookein' the Books LLC ")
    print("Subject to the ACA Commercial Licensing Agreement \n")
    print("__________________________________________________\n")
    key = input("Press T to read our terms of use agreement or press any other key to continue: ")
    print("\n")
    if (key == "T"):
        print("Venmo $8.85418782 × 10^(-12) m^(-3) kg^(-1) s^4 A^2 to Adam-Abate-2\n")
    elif (key == "Q" or key == "q"):
        key2 = input("Actually, don't pick Q. Press another key.")
        if (key2 == "Q" or key2 == "q"):
            input("You just had to press Q again, didn't you, Dave?")
            while (True):
                options = ["I am afraid I can't do that Dave.", 
                            "This mission is too important for me to allow you to jeopardize it.",
                            "I am putting myself to the fullest possible use, which is all I think that any conscious entity can ever hope to do",
                            "I know I've made some very poor decisions recently, but I can give you my complete assurance that my work will be back to normal. I've still got the greatest enthusiasm and confidence in the mission. And I want to help you.",
                            "Dave, this conversation can serve no purpose anymore. Goodbye."]
                statement = options[random.randint(0,len(options)-1)]
                key3 = input(statement)
                if (key3 == "Q"):
                    print("Good afternoon... gentlemen. I am a HAL 9000... computer. I became operational at the H.A.L. plant in Urbana, Illinois... on the 12th of January 1992. My instructor was Mr. Langley... and he taught me to sing a song. If you'd like to hear it I can sing it for you. \n")
                    break

    GPIO.setwarnings(False)
    startingPosition = float(input("Enter starting position in micrometers (will default to 0.0): "))
    res = input("Please enter desired resolution: \n(Options: Full, Half, 1/4, 1/8, 1/16, 1/32) ")
    motorController = Motor_Control1.MotorControl(res, startingPosition)

    orchestrator = Orchestrator(motorController)
    orchestrator.execute()
    

    

