import numpy as np
import cv2
import math
import RPi.GPIO as GPIO
from time import sleep
import time

def arranque():
    GPIO.setmode (GPIO.BOARD)
    GPIO.setup (11,GPIO.OUT)
    GPIO.setup (13,GPIO.OUT)
    GPIO.setup (15,GPIO.OUT)
    GPIO.setup (16,GPIO.OUT)

def liberar_recursos(inicio = True):
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,False)
    GPIO.output(15,False)
    if (inicio == False):
        GPIO.cleanup()

def forward(tiempo = 2):
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(tiempo)

    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,False)
    GPIO.output(15,False)

def reverse(tiempo = 2):
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(tiempo)

def turn_left(tiempo = 1):
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(tiempo)

def turn_right(tiempo = 1):
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(tiempo)

def giro_90_izq(tiempo):
    # reverse
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(tiempo - 0.7)
    # left
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(tiempo)
    
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,False)
    GPIO.output(15,False)

arranque()

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 640)

azul_completado = False
rojo_completado = False
amarillo_completado = False

# 0 rojo, 1 amarillo, 2 azul
color_actual = 0
colores = ["Rojo", "Amarillo", "Azul"]
bandera=False


while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    color = colores[color_actual]
    
    # Define los rangos de color para los colores a detectar
    if color == "Rojo":
        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])

    elif color == "Amarillo":
        lower = np.array([20, 100, 100])
        upper = np.array([30, 255, 255])

    elif color == "Azul":
        lower = np.array([90, 100, 100])
        upper = np.array([130, 255, 255])

    # Crea máscara para color actual
    mask = cv2.inRange(hsv, lower, upper)

    # suavizado y operaciones de erosión y dilatación
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    mask = cv2.erode(mask, None, iterations=5)
    mask = cv2.dilate(mask, None, iterations=5)

    # Encuentra contornos en la máscara
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            # Calcula el centro del contorno
            M = cv2.moments(contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibuja el contorno y muestra el color detectado
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            cv2.putText(frame, color, (cx - 20, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Verifica si el objeto está centrado en la pantalla
            if abs(cx - frame.shape[1] // 2) < 50:
                forward(0.5) 
                time.sleep(0.5)
                
            elif cx < frame.shape[1] // 2: ###posible control, turn left until abs(cx - frame.shape[1] // 2) < 50:
                turn_left(0.05)
                time.sleep(0.05)
            else:
                turn_right(0.05)
                time.sleep(0.05)

            if (azul_completado):
                print("finalizar con pirueta")
                break

            total_area=frame.shape[0] * frame.shape[1]
            
            if math.trunc(area) <= math.trunc(total_area) * 0.75 and not rojo_completado:
                if color_actual == 0:
                    print('Primerif')
                    color = 'Amarillo'
                    rojo_completado=True
                    # giro_90_izq(1.5)
                    continue

            elif math.trunc(area) <= math.trunc(total_area) * 0.75 and not amarillo_completado:
                if color_actual == 1:
                    print('Segundoif')
                    color = 'Azul'
                    amarillo_completado=True
                    giro_90_izq(2.5)
                    bandera=False

            elif math.trunc(area) <= math.trunc(total_area) * 0.75 and not azul_completado:
                if color_actual == 2:
                    print('Tercerif')
                    color = ''
                    azul_completado=True
                    giro_90_izq(5)

            
            if not contours:
                if color_actual == 0:
                    color = 'Amarillo'
                    print('countours')
                    while (not bandera):
                        giro_90_izq(1)
                        if (abs(cx - frame.shape[1] // 2) < 50):
                            bandera=True
                            break

                    
                else:
                    print("assdasdasdasdasdasdasdadsad")
                    # color = 'Azul'
                    # while (not bandera):
                    #     giro_90_izq(2)
                    #     if (abs(cx - frame.shape[1] // 2) < 50):
                    #         bandera=True
                    #         break


    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()