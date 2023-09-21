import cv2 
import imutils
import numpy as np

cap=cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

while true:
	ret, frame=cap.read()
	hsv=cv2.cvtColor(frame, cv2.COLORBGR2HSV)

	#amarillo
	amarillo_osc=np.array([25, 70, 120])
amarillo_cla=np.array([30, 255, 255])

#rojo
	rojo_osc=np.array([0, 50, 120])
rojo_cla=np.array([10, 255, 255])

	#azul
	azul_osc=np.array([90, 60, 120])
azul_cla=np.array([121, 255, 255])

cara1=cv2.inRange(hsv, amarillo_osc, amarillo_cla)
cara2=cv2.inRange(hsv, rojo_osc, rojo_cla)
cara3=cv2.inRange(hsv, azul_osc, azul_cla)

cnts1=cv2.findContours(cara1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts1=imutils.grab_contours(cnts1)

cnts2=cv2.findContours(cara2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts2=imutils.grab_contours(cnts2)

cnts3=cv2.findContours(cara3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts3=imutils.grab_contours(cnts3)

for c in cnts1:
area1=cv2.contourArea(c)
	if area1>5000:
cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
M=cv2.moments(c)
cx=int(M[‘m10’]/M[‘m00’])
cy=int(M[‘m01’]/M[‘m00’])
cv2.circle(frame, “Amarilo”, (cx-20, cy-20), cv2.FONT_ITALIC, 2 (255, 255, 255), 2)


for c in cnts2:
area2=cv2.contourArea(c)
if area2>5000:
cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
M=cv2.moments(c)
cx=int(M[‘m10’]/M[‘m00’])
cy=int(M[‘m01’]/M[‘m00’])
cv2.circle(frame, “Amarilo”, (cx-20, cy-20), cv2.FONT_ITALIC, 2 (255, 255, 255), 2)

for c in cnts3:
area3=cv2.contourArea(c)

if area3>5000:
cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
M=cv2.moments(c)
cx=int(M[‘m10’]/M[‘m00’])
cy=int(M[‘m01’]/M[‘m00’])
cv2.circle(frame, “Amarilo”, (cx-20, cy-20), cv2.FONT_ITALIC, 2 (255, 255, 255), 2)




cv2.imshow(“Video”, frame)
k=cv2.waitKey(1)
if k==27:
break

cap.release()
cv2.destroyAllWindows()
