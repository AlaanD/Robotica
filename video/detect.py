import torch
from models.experimental import attempt_load
from utils.general import non_max_suppression
import cv2

# Verifica si la GPU está disponible
if torch.cuda.is_available():
    # Configura el dispositivo para usar la GPU
    device = torch.device("cuda")
else:
    # Si no hay GPU, usa la CPU
    device = torch.device("cpu")

# Carga el modelo .pt
model = attempt_load('ruta/a/tu/modelo.pt', map_location=device)
model = model.to(device)

# Inicializa la cámara (en este caso, la cámara 0)
cap = cv2.VideoCapture(0)

while True:
    # Captura un fotograma de la cámara
    ret, frame = cap.read()
    
    if not ret:
        break

    # Realiza una inferencia en el fotograma
    img = frame.transpose(2, 0, 1)  # Transpone la imagen para que coincida con el formato del modelo
    img = torch.from_numpy(img).float() / 255.0  # Normaliza los valores de píxeles
    img = img.unsqueeze(0)  # Agrega una dimensión para el lote
    img = img.to(device)  # Mueve el fotograma a la GPU
    pred = model(img)

    # Realiza la supresión de no máxima
    pred = non_max_suppression(pred, conf_thres=0.25, iou_thres=0.45)

    # Procesa las detecciones
    for det in pred[0]:
        if det is not None and len(det):
            det[:, :4] = det[:, :4].clamp(0, frame.shape[1])  # Ajusta las coordenadas
            det = det[det[:, 4] > 0.25]  # Filtra detecciones débiles
            # Dibuja los cuadros delimitadores en el fotograma
            for box in det:
                x1, y1, x2, y2, conf, cls = box
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, str(cls), (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # Muestra el resultado en una ventana
    cv2.imshow('YOLOv5 Object Detection', frame)

    # Presiona la tecla 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra la ventana
cap.release()
cv2.destroyAllWindows()
