import cv2
import numpy as np

class Filter():
    def filter_white_background(self, imagen):
        #Cargamos la imagen
        self.image = cv2.imread(imagen)
        #Convertimos la imagen a una escala de grises
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #Creamos una máscara para poder los píxeles del fondo
        _, mask = cv2.threshold(self.gray, 240, 255, cv2.THRESH_BINARY)
        #Invertimos la máscara
        self.mask_invert = cv2.bitwise_not(self.mask)
        #Creamos un fondo blanco
        self.white_background = np.full_like(self.image, 255)
        #Aplicamos la máscara
        self.object = cv2.bitwise_and(self.image, self.image, Mask=self.mask_invert)
        #Se combina el objeto con el fondo blanco
        result = cv2.add(self.object, self.white_background)
        #Se puede dejar así o se puede convertir a imagen
        cv2.imwrite("Resultado_final_de_imagen.jpg", result)
        return result

    def filter_photo_cropping(self, imagen):
        #Cargamos la imagen
        self.image = cv2.imread(imagen)
        #Convertimos la imagen a una escala de grises
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        #Umbral para detección del objeto en primer plano
        _, umbral = cv2.threshold(self.gray, 150, 255, cv2.THRESH_BINARY)
        #Encontrar contornos
        self.contornos, _ = cv2.findContours(umbral, cv2.RETR_EXTERNAL, cv2. CHAIN_APPROX_SIMPLE)
        #Encontramos el área del objeto más grande
        self.x, self.y, self.w, self.h = cv2.boundingRect(self.contornos[0])
        #Recortamos la imagen
        crop = self.image[self.y:self.y+self.h, self.x:self.x+self.w]
        #Guardamos la imagen recortada
        cv2.imwrite("Resultado_final_de_imagen.jpg", crop)
        return crop

    def filter_background_remove(self, imagen):
        #Cargamos la imagen
        self.image = cv2.imread(imagen)
        #Creamos una máscara
        self.mask = np.zeros(self.image.shape[:2], np.uint8)
        #Definimos los modelos de fondo y la imagen
        self.bgdModel = np.zeros((1, 65), np.float64)
        self.fgdModel = np.zeros((1, 65), np.float64)
        #Definimos la región de interés
        self.rect = (50, 50, self.image.shape[1]-50, self.image.shape[0]-50)
        #Aplicamos el GrabCut
        cv2.grabCut(self.image, self.mask, self.rect, self.bgdModel, self.fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        #Creamos la máscara binaria
        self.final_mask = np.where((self.mask == 2) | (self.mask == 0), 0, 1).astype("uint8")
        final_image = self.image * self.final_mask[:, :, np.newaxis]
        return final_image

    def filter_change_size(self, imagen):
        #Cargamos la imagen
        self.image = cv2.imread(imagen)
        #Definimos el nuevo tamaño
        self.width, self.hight = 800, 600
        new_image = cv2.resize(self.image, (self.width, self.hight))
        return new_image

    def filter_fisheye(self, imagen):
        #Cargamos la imagen
        self.image = cv2.imread(imagen)
        self.hight, self.width = self.image.shape[:2]
        #Creamos una malla de coordenadas
        self.map_x = np.title(np.arange(self.width), (self.hight, 1)).astype(np.float32)
        self.map_y = np.title(np.arange(self.hight), (self.width, 1)).astype(np.float32)
        #Normalizar coordenadas
        self.cx, self.cy = self.width/2, self.hight/2 #Centro de la imagen
        self.radio_max = np.sqrt(self.cx**2 + self.cy**2)
        #Aplicar transformación de ojo de pez
        self.factor = 0.5 #Intensidad del efecto
        self.distance = np.sqrt((self.map_x - self.cx)**2 + (self.map_y - self.cy)**2)
        self.map_x = self.cx + (self.map_x - self.cx) * (1 - self.factor * (self.distance / self.radio_max))
        self.map_y = self.cy + (self.map_y - self.cy) * (1 - self.factor * (self.distance / self.radio_max))
        #Aplicamos el remapeo
        imagen_pez = cv2.remap(self.image, self.map_x, self.map_y, cv2.INTER_LINEAR)
        return imagen_pez

    def filter_chromatic_aberration(self, imagen):
        #Cargamos la image
        self.image = cv2.imread(imagen)
        self.b, self.g, self.r = cv2.split(self.image)
        #Desplazamos los canales para simular
        self.shift_x, self.shift_y = 5, 5 #Ajustar la intensidad
        self.columns, self.rows = self.image.shape[:2]
        #Creamos mapas de transformacion
        self.M_right = np.float32([[1, 0, self.shift_x], [0, 1, self.shift_y]])
        self.M_left = np.float32([[1, 0, -self.shift_x], [0, 1, -self.shift_y]])
        #Aplicamos el desplazamiento
        self.b_shifted = cv2.warpAffine(self.b, self.M_right, (self.columns, self.rows))
        self.r_shifted = cv2.warpAffine(self.r, self.M_left, (self.columns, self.rows))
        #Unimos los canales
        imagen_aberracion = cv2.merge([self.b_shifted, self.g, self.r_shifted])
        return imagen_aberracion

