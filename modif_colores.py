import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

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
            print(f"Estoy en el color {color_detected}")

    cv2.imshow("Video", frame)
    k = cv2.waitKey(1)
    if k == 113:
        break

cap.release()
cv2.destroyAllWindows()
