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
    liberar_recursos()

def reverse(tiempo = 2):
    GPIO.output(11,GPIO.HIGH)
    GPIO.output(13,GPIO.LOW)
    GPIO.output(16,GPIO.LOW)
    GPIO.output(15,GPIO.HIGH)
    time.sleep(tiempo)
    liberar_recursos()

def turn_left(tiempo = 1):
    GPIO.output(11,GPIO.LOW)
    GPIO.output(13,GPIO.HIGH)
    GPIO.output(16,False)
    GPIO.output(15,False)
    time.sleep(tiempo)
    liberar_recursos()

def turn_right(tiempo = 1):
    GPIO.output(11,False)
    GPIO.output(13,False)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(15,GPIO.LOW)
    time.sleep(tiempo)
    liberar_recursos()

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

def giro_130_izq():
    reverse(0.8)
    turn_left(2)

def vuelta_entera():
    reverse(1)
    turn_right(4)
    print("¡¡¡festejo!!!")

arranque()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

azul_completado = False

# 0 rojo, 1 amarillo, 2 azul
color_actual = 'Rojo'
colores = ["Rojo", "Amarillo", "Azul"]
aux = 0
area_prom = 0
contador = 0
busqueda_iniciada = False
empezar = True

k = cv2.waitKey(1)
j = True

while j:
    z = input("Ingrese s para saludar")
    if z == "s":
        print("arrancar")
        forward(1)
        reverse(1)
    z = ""
    z = input("Ingrese s para empezar")
    if z == "s":
        j = False

while not azul_completado and z == 's':
    ret, frame = cap.read()
    if not ret:
        break

    if empezar:
        cv2.imshow("Video", frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    color_actual = colores[aux]
    
    # Define los rangos de color para los colores a detectar
    if color_actual == "Rojo":
        lower = np.array([0, 100, 100])
        upper = np.array([10, 255, 255])
        
    elif color_actual == "Amarillo":
        lower = np.array([20, 100, 100])
        upper = np.array([30, 255, 255])

    elif color_actual == "Azul":
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
    if contours:
        busqueda_iniciada=False
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        contador += 1
        area_prom = (area_prom + area) / contador

        print("Área del contorno más grande:", area)

        if area >= area_prom:
            print("area > 500")
            # Calcula el centro del contorno
            M = cv2.moments(largest_contour)
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # Dibuja el contorno y muestra el color detectado
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)
            cv2.putText(frame, color_actual, (cx - 20, cy - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Verifica si el objeto está centrado en la pantalla
            if abs(cx - frame.shape[1] // 2) < 50:
                forward(0.07)
                print("adel")
                #comienzo=False

            elif cx < frame.shape[1] // 2:
                turn_left(0.02)
                print("izq")
            else:
                turn_right(0.02)
                print("der")

            if (azul_completado):
                vuelta_entera()

            total_area = frame.shape[0] * frame.shape[1]

            if math.trunc(area) >= math.trunc(total_area) * 0.75:
                aux+=1
                if (aux < 3):
                    color_actual = colores[aux]
                    print("meta: ", aux)
                    if(color_actual=='Amarillo'):
                        giro_90_izq(1.5)
                    elif(color_actual=='Azul'):
                        giro_130_izq()
                else:
                    azul_completado = True
                    vuelta_entera()

        # else:
        #     turn_right(0.3)
        #     reverse(0.5)
        #     print("else contours")

    else:
        if not busqueda_iniciada:
            reverse(0.3)
            busqueda_iniciada = True
        turn_right(0.05)
        print("buscando meta")

    cv2.imshow("Video", frame)
    empezar = False
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()
liberar_recursos(False)
