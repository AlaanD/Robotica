import RPi.GPIO as GPIO
from time import sleep
import time
import curses

def arranque():
    GPIO.setmode (GPIO.BOARD)
    GPIO.setup (11,GPIO.OUT)
    GPIO.setup (13,GPIO.OUT)
    GPIO.setup (15,GPIO.OUT)
    GPIO.setup (16,GPIO.OUT)

def liberar_recursos(inicio):
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,False)
    GPIO.output(15,False)
    if (inicio == False):
        GPIO.cleanup()

def forward():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(2)

def reverse():
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(2)

def turn_left():
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(1)

def turn_right():
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(1)

def main(letra):
    global tiempo_giro
    inicio = True
    while(inicio):
        curses.halfdelay(1)
        key = letra.getch()
        if key == 113:
            inicio = False
            liberar_recursos(inicio)
        elif key == 119:
            print("adelante")
            forward()
        elif key == 97:
            print("izquierda")
            turn_left()
            tiempo_giro = time.time() + 0.15
        elif key == 115:
            print("reversa")
            reverse()
            tiempo_giro = time.time() + 0.05

        elif key == 100:
            print("derecha")
            turn_right()
            tiempo_giro = time.time() + 0.5
        elif key == 101:
            print("detener")
            liberar_recursos(inicio)

        # Comprobar si el tiempo de giro ha pasado y detener el giro
        if tiempo_giro > 0 and time.time() >= tiempo_giro:
            liberar_recursos(inicio)
            tiempo_giro = 0

tiempo_giro = 0
arranque()
curses.wrapper(main)