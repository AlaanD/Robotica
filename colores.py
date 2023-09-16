import cv2
import imutils
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

while True:
    ret, frame=cap.read()
    if not ret:
         break
    hsv=cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    #amarillo
    amarillo_osc=np.array([20, 100, 100])
    amarillo_cla=np.array([30, 255, 255])

    #rojo
    rojo_osc=np.array([0, 100, 120])
    rojo_cla=np.array([10, 255, 255])

	#azul
    azul_osc=np.array([90, 100, 100])
    azul_cla=np.array([130, 255, 255])

    cara_amarillo=cv2.inRange(hsv, amarillo_osc, amarillo_cla)
    cara_rojo=cv2.inRange(hsv, rojo_osc, rojo_cla)
    cara_azul=cv2.inRange(hsv, azul_osc, azul_cla)

# Detección de contornos
    cnts_amarillo, _ = cv2.findContours(cara_amarillo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_rojo, _ = cv2.findContours(cara_rojo, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts_azul, _ = cv2.findContours(cara_azul, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for contour in cnts_amarillo:
    #     area = cv2.contourArea(contour)
    #     if area > 500:
    #         cv2.drawContours(frame, [contour], -1, (0, 255, 255), 3)
    #         print("Estoy en el amarillo")

    # for contour in cnts_rojo:
    #     area = cv2.contourArea(contour)
    #     if area > 500:
    #         cv2.drawContours(frame, [contour], -1, (0, 0, 255), 3)
    #         print("Estoy en el rojo")
    # for contour in cnts_azul:
    #         area = cv2.contourArea(contour)
    #         if area > 500:
    #             cv2.drawContours(frame, [contour], -1, (255, 0, 0), 3)
    #             print("Estoy en el azul")

    # cv2.imshow("Video", frame)
    # k = cv2.waitKey(1)
    # if k == 113:
    #     break

    # cap.release()
    # cv2.destroyAllWindows()







#     cnts_amarillo=cv2.findContours(cara_amarillo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnts_amarillo=imutils.grab_contours(cnts_amarillo)

#     cnts2=cv2.findContours(cara_rojo, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnts2=imutils.grab_contours(cnts2)

#     cnts3=cv2.findContours(cara_azul, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#     cnts3=imutils.grab_contours(cnts3)

    for c in cnts_amarillo:
        area1=cv2.contourArea(c)
        if area1>500:
            cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
            M=cv2.moments(c)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
            #cv2.circle(frame, (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            #cv2.circle(frame, "Amarilo", (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            print("estoy en el amarillo")

    for c in cnts_rojo:
        area2=cv2.contourArea(c)
        if area2>500:
            cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
            M=cv2.moments(c)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
            #cv2.circle(frame, "Amarilo", (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            #cv2.circle(frame, (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            print("estoy en el rojo")

    for c in cnts_azul:
        area3=cv2.contourArea(c)

        if area3>5000:
            cv2.drawContours(frame, [c], -1, (30, 255, 255), 3)
            M=cv2.moments(c)
            cx=int(M["m10"]/M["m00"])
            cy=int(M["m01"]/M["m00"])
            #cv2.circle(frame, "Amarilo", (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            #cv2.circle(frame, (cx-20, cy-20), cv2.FONT_ITALIC, 2, (255, 255, 255), 2)
            print("estoy en el azul")



    cv2.imshow("Video", frame)
    k=cv2.waitKey(1)
    if k==113:
        break

cap.release()
cv2.destroyAllWindows()
