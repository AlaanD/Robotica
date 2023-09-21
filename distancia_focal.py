import cv2
import math

# Altura del objeto, altura de la cámara y ángulo de inclinación de la cámara en grados
h_objeto = 0.08  # metros
h_camara = 0.09  # metros
angulo_grados = 0  # grados

# Cargar una imagen o capturar un fotograma desde una cámara
# En este ejemplo, cargaremos una imagen
imagen = cv2.imread('tu_imagen.jpg')

# Convertir el ángulo de grados a radianes
angulo_radianes = math.radians(angulo_grados)

# Calcular la distancia
distancia = (h_objeto - h_camara) / math.tan(angulo_radianes)

# Mostrar la distancia en la imagen
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(imagen, f'Distancia: {distancia:.2f} metros', (10, 30), font, 1, (0, 0, 255), 2)

# Mostrar la imagen con la distancia
cv2.imshow('Imagen con Distancia', imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()
