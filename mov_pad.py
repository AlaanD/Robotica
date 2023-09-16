import curses
import RPi.GPIO as gpio
import time
import pygame

def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

def forward(sec):
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

def turn_self(sec):
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
    running = True

    while(running):
        for event in pygame.event.get():

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == 9:
                    running = False
                    break
                elif event.button == 4:
                    print("adelante")
                    forward(sec)
                elif event.button == 3:
                    print("izquierda")
                    right_turn(sec)
                elif event.button == 0:
                    print("Giro en el lugar")
                    turn_self(sec)
                elif event.button == 1:
                    print("derecha")
                    left_turn(sec)
                else:
                    print("detenido")
        pygame.time.delay(10)


# Inicializar pygame
pygame.init()

# Verificar cuántos joysticks están conectados
num_joysticks = pygame.joystick.get_count()
if num_joysticks == 0:
    print("No se encontraron mandos conectados.")
    quit()

# Seleccionar el primer joystick
joystick = pygame.joystick.Joystick(0)
joystick.init()

curses.wrapper(main)
gpio.cleanup()


# seconds = 5
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

