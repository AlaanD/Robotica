import RPi.GPIO as GPIO
from time import sleep
import time
import curses

GPIO.setmode (GPIO.BOARD)
GPIO.setup (11,GPIO.OUT)
GPIO.setup (13,GPIO.OUT)
GPIO.setup (15,GPIO.OUT)
GPIO.setup (16,GPIO.OUT)

def forward():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(2)
    #GPIO.cleanup()

def reverse():
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(2)
    #GPIO.cleanup()

def turn_left():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(1)
    #GPIO.cleanup()

def turn_right():
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(1)
    #GPIO.cleanup()

def main(letra):
    inicio = True
    while(inicio):
        curses.halfdelay(1)
        key = letra.getch()
        if key == 113:
            inicio = False
        elif key == 119:
            print("adelante")
            forward()
        elif key == 97:
            print("izquierda")
            turn_left()
        elif key == 115:
            print("reversa")
            reverse()
        elif key == 100:
            print("derecha")
            turn_right()
        else:
            print("detenido")

curses.wrapper(main)
GPIO.cleanup()