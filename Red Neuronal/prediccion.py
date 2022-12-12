from tensorflow.python.keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np
import cv2

class prediccion():
    """
    Carga el modelo de la red neuronal de la ruta especificada
    """
    def __init__(self):
        self.rutaModelo="models/modeloReconocimientoNumeros.keras"
        self.model=load_model(self.rutaModelo)
        self.width=28
        self.heigth=28

    def predecir(self,imagen):
        """
            Toma la imagen de entrada y realiza el proceso de predicción
        """
        imagen=cv2.resize(imagen,(self.width,self.heigth))
        imagen=imagen.flatten()
        imagen=np.array(imagen)
        imagenNormalizada=imagen/255
        pruebas=[]
        pruebas.append(imagenNormalizada)
        imagenesAPredecir=np.array(pruebas)
        predicciones=self.model.predict(x=imagenesAPredecir)
        claseMayorValor=np.argmax(predicciones,axis=1)
        print(predicciones)
        print (claseMayorValor)
        return claseMayorValor[0]


categorias=["0","1","2","3","4","5","6","7","8","9"]
reconocimiento=prediccion()
imagenPrueba=cv2.imread("test/1/1_19.jpg",0)
indiceCategoria=reconocimiento.predecir(imagenPrueba)
print("La imamgen cargada es ",categorias[indiceCategoria])


if imagenPrueba is None:
  print("error al cargar la imagen")
else:
  plt.imshow(cv2.cvtColor(imagenPrueba, cv2.COLOR_BGR2RGB))
  plt.axis("off")
  plt.show()