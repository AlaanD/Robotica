import RPi.GPIO as GPIO
from time import sleep
import time

GPIO.setmode (GPIO.BOARD)
GPIO.setup (11,GPIO.OUT)
GPIO.setup (13,GPIO.OUT)
GPIO.setup (15,GPIO.OUT)
GPIO.setup (16,GPIO.OUT)

# while True:
#     GPIO.output(11,True)
#     time.sleep(2)
#     GPIO.output(11,False)
#     time.sleep(2) 

def reverse():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(2)
    GPIO.cleanup()

def forward():
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(2)
    GPIO.cleanup()

def turn_right():
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(2)
    GPIO.cleanup()

def turn_left():
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(2)
    GPIO.cleanup()

turn_left()
