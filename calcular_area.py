import numpy as np
import cv2

# Inicializar la cámara
camara = cv2.VideoCapture(0)  # 0 representa la cámara web predeterminada (puedes cambiarlo si tienes múltiples cámaras)

if not camara.isOpened():
    print("Error: No se pudo abrir la cámara.")
else:
    while True:
        # Capturar un fotograma de la cámara
        ret, frame = camara.read()

        if ret:
            cv2.imwrite("captura.jpg", frame)

            # Leer imagen
            imagen = cv2.imread("captura.jpg")

            # Convertir la imagen a escala de grises (si es necesario)
            imagen_gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

            # Realizar umbralización (si es necesario)
            _, imagen_umbralizada = cv2.threshold(imagen_gris, 128, 255, cv2.THRESH_BINARY)

            # Encontrar contornos en la imagen
            contornos, _ = cv2.findContours(imagen_umbralizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Calcular el área del objeto (por ejemplo, el primer contorno encontrado)
            if len(contornos) > 0:
                area_objeto = cv2.contourArea(contornos[0])
                print("Área del objeto:", area_objeto)
            else:
                print("No se encontraron contornos en la imagen.")

            # Mostrar la imagen con los contornos resaltados (opcional)
            cv2.drawContours(imagen, contornos, -1, (0, 255, 0), 2)
            cv2.imshow('Imagen con contornos', imagen)

            # Esperar a que se presione una tecla durante un breve periodo (1 milisegundo)
            key = cv2.waitKey(1) & 0xFF

            # Salir del ciclo si se presiona la tecla 'q'
            if key == ord('q'):
                break

    # Liberar la cámara
    camara.release()

cv2.destroyAllWindows()
