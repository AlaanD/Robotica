import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Inicializa el contador
count = 0

# Bucle infinito
while True:
    
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Video", frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

    # Si se presiona cualquier otra tecla, guarda el fotograma como una imagen
    elif (k == 113):
        # Incrementa el contador
        count += 1

        # Crea el nombre del archivo de imagen usando el contador
        filename = "frame" + str(count) + ".jpg"

        # Guarda el fotograma como una imagen
        cv2.imwrite(filename, frame)

# Libera el objeto VideoCapture y destruye todas las ventanas
cap.release()
cv2.destroyAllWindows()
