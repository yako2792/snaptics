import cv2
import numpy as np

class Filter():
    def filter_white_background(imagen):
        #Cargamos la imagen
        image = cv2.imread(imagen)
        #Convertimos la imagen a una escala de grises
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        #Creamos una máscara para poder los píxeles del fondo
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
        #Invertimos la máscara
        mask_invert = cv2.bitwise_not(mask)
        #Creamos un fondo blanco
        white_background = np.full_like(image, 255)
        #Aplicamos la máscara
        object = cv2.bitwise_and(image, image, Mask=mask_invert)
        #Se combina el objeto con el fondo blanco
        result = cv2.add(object, white_background)
        #Se puede dejar así o se puede convertir a imagen
        cv2.imwrite("Resultado_final_de_imagen.png", result)
        return result
