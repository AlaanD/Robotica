import cv2

video = cv2.VideoCapture('video.mp4')

while (video.isOpened()):
    ret, frame = video.read()

    frame = cv2.resize(frame,(1080,800))
    if ret == True:
        
        texto1 = 'FPS: ' + str(int(video.get(cv2.CAP_PROP_FPS)))
        texto2 = 'Width: '+ str(int(video.get(cv2.CAP_PROP_FRAME_WIDTH)))
        texto3 = 'Height: '+ str(int(video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        cv2.putText(frame, texto1, (900,20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, texto2, (900,40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, texto3, (900,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        cv2.imshow('Reproducion video', frame)

        if cv2.waitKey(1) == ord('e'):
            break
    else: break

video.release()
cv2.destroyAllWindows()