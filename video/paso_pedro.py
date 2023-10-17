from gpiozero import Robot,PWMOutputDevice
from time import sleep
import time
import cv2
import numpy as np

robot = Robot(left = (17, 22), right = (23, 24))
encontro_rojo = False
encontro_azul = False
encontro_amarillo = False
saludo = False
desired_speed = 0.6

def marchaAdelante():
    robot.forward(speed=desired_speed)    
    
def detenerse():
    robot.stop()
    sleep(2)
    
def girar_izquierda90():
    # Gira a la izquierda
    robot.left(speed=desired_speed)  
    sleep(0.60)    
      
      
def girar_izquierda135():
    # Gira a la izquierda
    robot.left(speed=desired_speed)  
    sleep(0.6005) 

# def detectar_azul(frame):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     
#     # Define el rango de colores azules en HSV
#     lower_blue = np.array([90, 50, 50])
#     upper_blue = np.array([130, 255, 255])
# 
#     # Crea una máscara para el color azul
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
# 
#     # Calcula el área de la máscara (pixeles azules)
#     blue_area = np.sum(mask > 0)
# 
#     # Calcula el área total de la imagen
#     total_area = frame.shape[0] * frame.shape[1]
# 
#     # Calcula el porcentaje de azul en la imagen
#     blue_percentage = (blue_area / total_area) * 100
# 
#     # Imprime 'azul' si más del 95% de la imagen es azul
#     if blue_percentage < 60:
#         marchaAdelante()
#     else:
#         detenerse()
#         return True
#         
#     return False
# 
# def detectar_rojo(frame):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     
#     # Define el rango de colores azules en HSV
#     lower_red = np.array([0, 100, 100])
#     upper_red = np.array([10, 255, 255])
# 
#     # Crea una máscara para el color azul
#     mask = cv2.inRange(hsv, lower_red, upper_red)
# 
#     # Calcula el área de la máscara (pixeles azules)
#     red_area = np.sum(mask > 0)
# 
#     # Calcula el área total de la imagen
#     total_area = frame.shape[0] * frame.shape[1]
# 
#     # Calcula el porcentaje de azul en la imagen
#     red_percentage = (red_area / total_area) * 100
# 
#     # Imprime 'azul' si más del 95% de la imagen es azul
#     if red_percentage < 60:
#         marchaAdelante()
#     else:
#         detenerse()
#         girar_izquierda90()
#         return True
#         
#     return False
# 
# def detectar_amarillo(frame):
#     hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#     
#     # Define el rango de colores amarillo en HSV
#     lower_yellow = np.array([20, 100, 100])
#     upper_yellow = np.array([30, 255, 255])
#     
#     # Crea una máscara para el color azul
#     mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
# 
#     # Calcula el área de la máscara (pixeles azules)
#     yellow_area = np.sum(mask > 0)
# 
#     # Calcula el área total de la imagen
#     total_area = frame.shape[0] * frame.shape[1]
# 
#     # Calcula el porcentaje de azul en la imagen
#     yellow_percentage = (yellow_area / total_area) * 100
# 
#     # Imprime 'azul' si más del 95% de la imagen es azul
#     if yellow_percentage < 60:
#         marchaAdelante()
#     else:
#         detenerse()
#         girar_izquierda135()
#         return True
#         
#     return False

def saludar():
    global saludo
    robot.left(speed=desired_speed)  
    sleep(0.4)
    robot.right(speed=desired_speed)  
    sleep(0.4)
    detenerse()
    saludo = True

# Carga las imagenes que quieres detectar en escala de grises
imagen_pare = cv2.imread('pare2.png', 0)
imagen_adelante = cv2.imread('adelante.png', 0)
imagen_balneario = cv2.imread('balneario.png', 0)
imagen_izquierda = cv2.imread('izquierda.png', 0)
imagen_derecha = cv2.imread('derecha.png', 0)
imagen_prohibido_u = cv2.imread('prohibido-u.png', 0)

# Inicializar la cámara (puedes cambiar el número 0 por la URL de un flujo de video si estás usando una cámara IP)
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


# Inicializar el detector SIFT
sift = cv2.SIFT_create()



# Umbral para la correspondencia
umbral = 0.7


def encontrarPare(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_pare, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)

    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre el pare nashe')
        
def encontrarAdelante(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_adelante, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)
    
    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre adelante nashe')
        
def encontrarBalneario(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_balneario, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)
    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre balneario nashe')
        
def encontrarIzquierda(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_izquierda, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)

    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre izquierda nashe')
        
def encontrarDerecha(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_derecha, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)
    
    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre derecha nashe')
        
def encontrarProhibidoU(frame):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(imagen_prohibido_u, None)
    
    # Convertir el frame a escala de grises
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    
    frame_gris_redimensionada = cv2.resize(frame_gris, (nuevo_ancho, nuevo_alto))

    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)
    
    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('me prohibieron girar en u pero igual voy a girar nashe')

while True:
    # Capturar un frame del flujo de video
    ret, frame = cap.read()
    if not ret:
        break

    encontrarPare(frame)
    #encontrarAdelante(frame)
    #encontrarBalneario(frame)
    #encontrarIzquierda(frame)
    #encontrarDerecha(frame)
    #encontrarProhibidoU(frame)
    

    # Mostrar el frame con la detección (imagen y mensaje)
    cv2.imshow('Video', frame)
 
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()
