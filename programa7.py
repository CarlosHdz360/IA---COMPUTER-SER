import cv2
import numpy as np
# se da un entrenamiento para que identifique que caracteristicas cuenta cada figura
def detectar_formas(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)
    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in cnts:
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        x, y, w, h = cv2.boundingRect(approx)
        if len(approx) == 3:
            cv2.putText(frame, 'Triangulo', (x, y-5), 1, 1, (0, 255, 0), 1)
        elif len(approx) == 4:
            aspect_ratio = float(w) / h
            if 0.95 <= aspect_ratio <= 1.05: 
                cv2.putText(frame, 'Cuadrado', (x, y-5), 1, 1, (0, 255, 0), 1)
            else:
                cv2.putText(frame, 'Rectangulo', (x, y-5), 1, 1, (0, 255, 0), 1)
        elif len(approx) == 5:
            cv2.putText(frame, 'Pentagono', (x, y-5), 1, 1, (0, 255, 0), 1)
        elif len(approx) == 6:
            cv2.putText(frame, 'Hexagono', (x, y-5), 1, 1, (0, 255, 0), 1)
        elif len(approx) > 10:
            cv2.putText(frame, 'Circulo', (x, y-5), 1, 1, (0, 255, 0), 1)

        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)

    return frame
#abre la cámara para derectar de que figura se trata 
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_con_formas = detectar_formas(frame)
    
    cv2.imshow('Deteccion de Formas', frame_con_formas)
    #Cierra si se presiona la tecla Esc
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()