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
    #reverse
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(tiempo - 0.7)

    #left
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(tiempo)

    #clean res
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,False)
    GPIO.output(15,False)

tiempo_giro = 0
arranque()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
azul_completado = False
rojo_completado = False
amarillo_completado = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define los rangos de color para los colores a detectar
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    red_lower = np.array([0, 100, 100])
    red_upper = np.array([10, 255, 255])

    blue_lower = np.array([90, 100, 100])
    blue_upper = np.array([130, 255, 255])

    # Crea máscaras para cada color
    mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)
    mask_red = cv2.inRange(hsv, red_lower, red_upper)
    mask_blue = cv2.inRange(hsv, blue_lower, blue_upper)

    # Combina las máscaras para detectar varios colores
    combined_mask = cv2.bitwise_or(mask_yellow, cv2.bitwise_or(mask_red, mask_blue))

    # Encuentra contornos en la máscara combinada
    contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)

        if area > 500:
            # Calcula el centro del contorno
            M = cv2.moments(contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Detecta el color predominante en el área del contorno
            color_detected = ""
            if cv2.pointPolygonTest(contour, (cx, cy), False) != -1:
                if mask_yellow[cy, cx] == 255:
                    color_detected = "Amarillo"
                elif mask_red[cy, cx] == 255:
                    color_detected = "Rojo"
                elif mask_blue[cy, cx] == 255:
                    color_detected = "Azul"

            # Dibuja el contorno y muestra el color detectado
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
            cv2.putText(frame, color_detected, (cx - 20, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Calcula el área total de la imagen
            total_area = frame.shape[0] * frame.shape[1]

            # Si el area es menor 75%
            if math.trunc(area) <= math.trunc(total_area) * 0.75 and not azul_completado:
                if(color_detected == 'Azul'):
                    forward(15)
                    azul_completado = True

            # Verifica si el área del contorno es igual al área total (75%)
            if math.trunc(area) >= math.trunc(total_area) * 0.75 and not azul_completado:
                if(color_detected == 'Azul'):
                    giro_90_izq(1.3)
                    azul_completado = True
                    
                    
    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()
