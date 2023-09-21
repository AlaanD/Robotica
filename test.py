import curses
import RPi.GPIO as gpio
import time


def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

def turn_self(sec):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup() 

def right_turn(sec):
    init()
    gpio.output(17, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()
    
def left_turn(sec):
    init()
    gpio.output(17, False)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
    gpio.cleanup()

def forward(sec):
    init()

    # GIRO EN EL LUGAR 
    gpio.output(17, True)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)

    time.sleep(sec)
    gpio.cleanup()

def main(letra):
    sec = 1
    while(True):
        curses.halfdelay(1)
        key = letra.getch()
        #print key
        if key == 113:
            break
        elif key == 119:
            print("adelante")
            forward(sec)
        elif key == 97:
            print("izquierda")
            right_turn(sec)
        elif key == 115:
            print("Giro en el lugar")
            turn_self(sec)
        elif key == 100:
            print("derecha")
            left_turn(sec)
        else:
            print("detenido")

curses.wrapper(main)
gpio.cleanup()


seconds = 5
# time.sleep(seconds)
# print("forward")
# forward(seconds)
# print("left turn")
# left_turn(seconds)
# print("right turn")
# right_turn(seconds)
# print("reverse")
# reverse(seconds)
# print("forward")
# forward(seconds)
main()
time.sleep(seconds-2)
gpio.cleanup()

