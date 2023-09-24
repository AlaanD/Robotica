import numpy as np
import cv2
import math
# import RPi.GPIO as GPIO
from time import sleep
from time import time



def arranque():
    print("arranque")


def liberar_recursos(inicio=True):
    print("libere recursos")


def forward(tiempo=2):
    print("adelante")


def reverse(tiempo=2):
    print("atras")


def turn_left(tiempo=1):
    print("izquierda")


def turn_right(tiempo=1):
    print("derecha")


def giro_90_izq(tiempo):
    # reverse
    print("90° izq")


tiempo_giro = 0
arranque()

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 640)
azul_completado = False
rojo_completado = False
amarillo_completado = False
# 0 rojo, 1 amariillo, 2 azul
color_actual = 0
colores = ["Rojo", "Amarillo", "Azul"]
max_no_detection_time = 2
no_detection_timer = time()

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
                forward(0.5)  # Avanza si el objeto está centrado

            if (color_actual == 3):
                print("finalizar con pirueta")
                break

            if math.trunc(area) >= math.trunc(frame.shape[0] * frame.shape[1] * 0.60):
                if color_actual == 0:
                    color = 'Amarillo'
                else:
                    color = 'Azul'

                color_actual += 1

            elif cx < frame.shape[1] // 2:
                turn_left(0.5)
            else:
                turn_right(0.5)

            if not contours:
                current_time = time()
                if current_time - no_detection_timer >= max_no_detection_time:
                    if color_actual == 0:
                        color = 'Amarillo'
                    else:
                        color = 'Azul'
                    color_actual += 1
                    no_detection_timer = current_time  # Reinicia temporizador
                    turn_left(1)

    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()
