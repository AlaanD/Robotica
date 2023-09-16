import RPi.GPIO as GPIO
from time import sleep

# Pins for Motor Driver Inputs 
Motor1A = 17
Motor1B = 22
Motor1C = 23
Motor1D = 27


def setup():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)              # GPIO Numbering
    GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1C,GPIO.OUT)
    GPIO.setup(Motor1D,GPIO.OUT)

def loop():
    # Going forwards
    GPIO.output(Motor1A,GPIO.HIGH)
    GPIO.output(Motor1B,GPIO.LOW)    #dejando 1b y 1c se mueven las izquierdas
    GPIO.output(Motor1C,GPIO.HIGH)
    GPIO.output(Motor1D,GPIO.LOW)
    
 
    sleep(5)
    # Going backwards
    # GPIO.output(Motor1A,GPIO.LOW)
    # GPIO.output(Motor1B,GPIO.HIGH)
    # GPIO.output(Motor1C,GPIO.HIGH)
    # GPIO.output(Motor1D,GPIO.LOW)
    #print("Going backwards")
 
    sleep(5)
    # Stop
    GPIO.output(Motor1C,GPIO.LOW)
    GPIO.output(Motor1A,GPIO.LOW)
    print("Stop")

def destroy():  
    GPIO.cleanup()

# if __name__ == '_main_':     # Program start from here
setup()
try:
    loop()
except KeyboardInterrupt:
    destroy()