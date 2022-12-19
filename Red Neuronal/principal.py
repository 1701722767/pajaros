import matplotlib.pyplot as plt
import numpy as np
import math
import cv2

## Import the keras API
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import InputLayer, Input
from tensorflow.python.keras.layers import Reshape, MaxPooling2D
from tensorflow.python.keras.layers import Conv2D, Dense, Flatten
from tensorflow.keras.optimizers import Adam

#Cargar datos de ejemplo
import tensorflow as tf

def cargarDatos(fase,numeroCategorias,limite):
    imagenesCargadas=[]
    etiquetas=[]
    valorEsperado=[]
    i=0
    for categoria in numeroCategorias:
        print(categoria)
        for idImagen in range(0,limite):
            salida=""
            if idImagen<10:
                salida="000"+str(idImagen)
            elif idImagen<100:
                salida="00"+str(idImagen)
            elif idImagen<1000:
                salida="0"+str(idImagen)
            else:
                salida=str(idImagen)
            ruta=fase+str(categoria)+"/"+str(categoria)+"_"+salida+".jpg"
            imagen=cv2.imread(ruta,0)
            if(imagen is not None):
                print(ruta)
                imagen=imagen.flatten()
                imagen=imagen/255
                imagenesCargadas.append(imagen)
                etiquetas.append(categoria)
                probabilidades=np.zeros(len(numeroCategorias))
                probabilidades[i]=1
                valorEsperado.append(probabilidades)
        i=i+1
    imagenesEntrenamiento=np.array(imagenesCargadas)
    etiquetasEntrenamiento=np.array(etiquetas)
    valoresEsperados=np.array(valorEsperado)
    return imagenesEntrenamiento,etiquetasEntrenamiento,valoresEsperados

img_size=21
img_size_2=28
#Numero de neuronas de la cnn
img_size_flat=img_size*img_size_2
#Parametrizar la forma de imagenes
num_chanels=1
#RGB, HSV -> num_chanels=3
img_shape=(img_size,img_size_2,num_chanels)
num_clases=['americano','basket','beisball','boxeo','ciclismo','f1','futbol','golf','natacion','tenis']
limiteImagenesPrueba=10000
imagenes,etiquetas,probabilidades=cargarDatos("sportimages/",num_clases,limiteImagenesPrueba)

model=Sequential()
#Capa entrada
model.add(InputLayer(input_shape=(img_size_flat,)))
#Reformar imagen
model.add(Reshape(img_shape))

#Capas convolucionales
model.add(Conv2D(kernel_size=5,strides=1,filters=16,padding='same',activation='relu',name='capa_convolucion_1'))
model.add(MaxPooling2D(pool_size=2,strides=2))

model.add(Conv2D(kernel_size=5,strides=1,filters=36,padding='same',activation='relu',name='capa_convolucion_2'))
model.add(MaxPooling2D(pool_size=2,strides=2))

#Aplanar imagen
model.add(Flatten())
#Capa densa
model.add(Dense(128,activation='linear'))


#Capa salida
model.add(Dense(len(num_clases),activation='softmax'))

optimizador=Adam(lr=1e-3)
model.compile(optimizer='Adam',
              loss='categorical_crossentropy',
              metrics=['accuracy']
)

model.fit(x=imagenes,y=probabilidades,epochs=6,batch_size=64)

limiteImagenesPrueba=3000
imagenesPrueba,etiquetasPrueba,probabilidadesPrueba=cargarDatos('sportimages/',num_clases,limiteImagenesPrueba)
resultados=model.evaluate(x=imagenesPrueba,y=probabilidadesPrueba)
print("{0}: {1:.2%}".format(model.metrics_names[1], resultados[1]))
#Carpeta y nombre del archivo como se almacenará el modelo
nombreArchivo='models/modeloReconocimientoNumeros2.keras'
model.save(nombreArchivo)
model.summary()