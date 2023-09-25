import numpy as np
import cv2
import math
import RPi.GPIO as GPIO
from time import sleep
import time
# import threading
# import queue

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

arranque()

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 640)

azul_completado = False
rojo_completado = False
amarillo_completado = False

# 0 rojo, 1 amarillo, 2 azul
color_actual = 2
colores = ["Rojo", "Amarillo", "Azul"]
bandera = False
comienzo = True

# # Cola de mensajes para comunicar el fotograma capturado
# frame_queue = queue.Queue()

# # Función para mostrar el video en un hilo separado
# def mostrar_video():
#     while True:
#         frame = frame_queue.get()
#         if frame is None:
#             break
#         cv2.imshow("Video", frame)
#         k = cv2.waitKey(1)
#         if k == 113:
#             break

# # Crea un hilo para mostrar el video
# video_thread = threading.Thread(target=mostrar_video)

# # Inicia el hilo del video
# video_thread.start()

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

    #para esperar el procesamiento de la nueva captura de la imagen
    # if (comienzo):
    #     time.sleep(1)
    #     comienzo = False
    # else:
    #     time.sleep(0.1)

    # # Coloca una copia del fotograma en la cola
    # frame_queue.put(frame.copy())

    #print("while")
    for contour in contours:
        
        area = cv2.contourArea(contour)
        print(area)

        if area > 500:
            print("area > 500")
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
                forward(1.5)
                comienzo = False
                print("adel")

            elif cx < frame.shape[1] // 2: #posible control, turn left until abs(cx - frame.shape[1] // 2) < 50:
                turn_left(0.05)
                print("izq")
            else:
                turn_right(0.05)
                print("der")

            if (azul_completado):
                print("finalizar con pirueta")
                break

            total_area = frame.shape[0] * frame.shape[1]
            
            #Si el area es menor 75%
            # if math.trunc(area) <= math.trunc(total_area) * 0.75 and not azul_completado:
            #     if(color == 'Azul'):
            #         forward(3)

            if math.trunc(area) >= math.trunc(total_area) * 0.75 and not azul_completado:
                if color_actual == 2:
                    print('Tercerif')
                    color = ''
                    azul_completado = True
                    giro_90_izq(1.3)

        # elif (area < 100 and comienzo == False):
        #     turn_right(0.3)
        #     print("area < 500")

    if (len(contours) ==  0):
        turn_right(0.3)
        reverse(0.5)
        print("contours 0")
        print(area)

    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 113:
        break

# # Coloca un valor especial en la cola para indicar al hilo de video que debe detenerse
# frame_queue.put(None)

# # Espera a que el hilo del video termine antes de liberar recursos
# video_thread.join()

cap.release()
cv2.destroyAllWindows()
liberar_recursos(False)