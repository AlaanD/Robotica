import torch
import cv2
import numpy as np

#lectura modelo
model=torch.hub.load('ultralytics/yolov5', 'custom',
                      path='/model/carteles.pt')

cap=cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    detect=model(frame)
    cv2.imshow('Detector de señales de transito', np.squeeze(detect.render()))

    t=cv2.watKey(5)
    if t==27:
        break

cap.release()
cv2.destroyAllWindows()








