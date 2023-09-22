# Importar librerías
import numpy as np
import cv2
import math

# Inicializar la cámara
camara = cv2.VideoCapture(0)  # 0 representa la cámara web predeterminada (puedes cambiarlo si tienes múltiples cámaras)

if not camara.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    # Capturar un fotograma de la cámara
    ret, frame = camara.read()

    if ret:
       
        cv2.imwrite("captura.jpg", frame)

        # Leer imagen
        img = cv2.imread("captura.jpg")

        # Convertir a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicar filtro de Canny
        edges = cv2.Canny(gray, 50, 150)

        # Encontrar contornos
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Dibujar contornos sobre la imagen original
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)

        # Calcular el área de cada contorno
        areas = [cv2.contourArea(c) for c in contours]

        # Seleccionar los dos contornos más grandes
        sorted_areas = np.argsort(areas)
        cnt1 = contours[sorted_areas[-1]] # Objeto a medir
        cnt2 = contours[sorted_areas[-2]] # Objeto de referencia

        # Calcular el ancho en píxeles de cada contorno
        rect1 = cv2.minAreaRect(cnt1)
        box1 = cv2.boxPoints(rect1)
        box1 = np.int0(box1)
        w1 = max(rect1[1]) # Ancho del objeto a medir

        rect2 = cv2.minAreaRect(cnt2)
        box2 = cv2.boxPoints(rect2)
        box2 = np.int0(box2)
        w2 = max(rect2[1]) # Ancho del objeto de referencia

        # Dibujar los rectángulos mínimos sobre la imagen original
        cv2.drawContours(img,[box1],0,(0,0,255),2)
        cv2.drawContours(img,[box2],0,(255,0,0),2)

        # Definir el tamaño del objeto de referencia (hoja A4) en centímetros
        W = 21

        # Definir la distancia del objeto de referencia a la cámara en centímetros
        D = 30

        # Calcular la distancia focal de la cámara
        f = (w2 * D) / W

        # Calcular la distancia del objeto a medir a la cámara
        d = (W * f) / w1

        # Mostrar el resultado en la pantalla
        print("La distancia del objeto a medir a la cámara es: {:.2f} cm".format(d))

        # Mostrar la imagen con los contornos y los rectángulos
        cv2.imshow("Imagen", img)
        cv2.waitKey(0)

    # Liberar la cámara
    camara.release()

# Cerrar las ventanas de OpenCV
cv2.destroyAllWindows()