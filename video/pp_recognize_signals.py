import cv2

cap = cv2.VideoCapture(0)

    # possible = cap.set(cv2.CAP_PROP_MODE, cv2.CAP_MODE_GRAY)
    # print(possible) No se puede capturar en escala de grises, convertir frame a frame

cap.set(3, 640)
cap.set(4, 480)

imagen_pare = cv2.imread('pare2.png', 0)
imagen_adelante = cv2.imread('adelante.png', 0)
imagen_balneario = cv2.imread('balneario.png', 0)
imagen_izquierda = cv2.imread('izquierda.png', 0)
imagen_derecha = cv2.imread('derecha.png', 0)
imagen_prohibido_u = cv2.imread('prohibido-u.png', 0)
pare_found = False
adelante_found = False
balneario_found = False
izquierda_found = False
derecha_found = False
prohibido_u_found = False
sift = cv2.SIFT_create()
umbral = 0.7

# Encontrar puntos clave y descriptores con SIFT
def encontrar(grey_frame, image_to_find):
    # Encuentra los puntos clave y descriptores de la imagen a detectar
    keypoints1, descriptors1 = sift.detectAndCompute(image_to_find, None)


    #Already tested resize the image outside the function to reduce time but it does the oppose
    nuevo_ancho = frame.shape[1] // 2
    nuevo_alto = frame.shape[0] // 2
    frame_gris_redimensionada = cv2.resize(grey_frame, (nuevo_ancho, nuevo_alto))
    # Encontrar puntos clave y descriptores del frame
    keypoints2, descriptors2 = sift.detectAndCompute(frame_gris_redimensionada, None)


    # Configurar el algoritmo de correspondencia
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)

    # Aplicar la razón de Lowe para filtrar las correspondencias
    good_matches = []
    for m, n in matches:
        if m.distance < umbral * n.distance:
            good_matches.append(m)

    # Si hay suficientes correspondencias, encontrar la señal detectada
    if len(good_matches) > 20:
        print('encontre el pare nashe')

step = 0
while True:
    # Capturar un frame del flujo de video
    ret, frame = cap.read()
    if not ret:
        break

    grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   
    cv2.imshow('VideoGrises', grey_frame)

    k = cv2.waitKey(800) #reduce fps to 1.25 per second to not accumulate frames
    if k == 113:  # Presionar 'q' para salir
        break
    
    if step == 0:
        encontrar(grey_frame, imagen_pare)
        if pare_found:
            step = 1
    elif step == 1:
        encontrar(grey_frame, imagen_adelante)
        if adelante_found:
            step = 2
    elif step == 2:
        encontrar(grey_frame, imagen_balneario)
        if balneario_found:
            step = 3
    elif step == 3:
        encontrar(grey_frame, imagen_izquierda)
        if izquierda_found:
            step = 4
    elif step == 4:
        encontrar(grey_frame, imagen_derecha)
        if derecha_found:
            step = 5
    elif step == 5:
        encontrar(grey_frame, imagen_prohibido_u)
        if prohibido_u_found:
            step = 6
    else:
        print('finished')
        break

cap.release()  # Liberar la cámara
cv2.destroyAllWindows()  # Cerrar ventanas de visualización