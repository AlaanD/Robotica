import cv2

image = cv2.imread('p/objeto_1.jpg')

majinBooClassif = cv2.CascadeClassifier('cascade.xml')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
toy = majinBooClassif.detectMultiScale(gray,
                                        scaleFactor = 5,
                                        minNeighbors = 91,
                                        minSize=(70,78))

for (x,y,w,h) in toy:
    cv2.rectangle(image, (x,y),(x+w,y+h),(0,255,0),2)
    cv2.putText(image,'Adelante',(x,y-10),2,0.7,(0,255,0),2,cv2.LINE_AA)

cv2.imshow('image',image)

cv2.waitKey(0)
cv2.destroyAllWindows()