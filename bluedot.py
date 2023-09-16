from gpiozero import Robot
from time import sleep
import Bluedot
bd = Bluedot()
robot = Robot(left=(7, 8), right=(9, 10))


def move(pos):
    if(pos.top):
        robot.forward()
        sleep(0.1)
    if(pos.bottom):
        robot.backwards()
        sleep(0.1)
    if(pos.right):
        robot.right()
        sleep(0.1)
    if(pos.left):
        robot.left()
        sleep(0.1)
    
def stop():
    robot.stop()

bd.when_press = move()
bd.when_moved = move()
db.when_released = stop()