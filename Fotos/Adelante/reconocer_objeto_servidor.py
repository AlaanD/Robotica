import torch
import cv2
import numpy as np

print(torch.__version__)
image = cv2.imread('p/objeto_1.jpg')

#lectura modelo
model=torch.hub.load('ultralytics/yolov5', 'custom',
                      path='/model/carteles.pt')


detect=model(image)
cv2.imshow('Detector de señales de transito', np.squeeze(detect.render()))

t = cv2.watKey(5)

cv2.destroyAllWindows()