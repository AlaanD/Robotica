import torch
import cv2
import numpy as np

print(torch.__version__)
image = cv2.imread('p/objeto_0.jpg')

#lectura modelo
model=torch.hub.load('ultralytics/yolov5', 'custom',
                      path='model\carteles.pt')


detect=model(image)
cv2.imshow('Detector de señales de transito', np.squeeze(detect.render()))

while True:
    key = cv2.waitKey(5)
    if key == 27:  # Check if the pressed key is 'Esc' (ASCII code 27)
        break

cv2.destroyAllWindows()
