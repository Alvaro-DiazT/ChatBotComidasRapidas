#Permite trabajar el procesamiento de lenguaje natural
import nltk
#transformar palabras
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import json
import random
import csv



# para guardar nuestro modelo( y no mantener cargandolo
import pickle
nltk.download('punkt')
#Para abrir el archivo json
with open("contenido.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)


try:
    with open("variables.pickle", "rb") as archivoPickle:
        palabras, tags, entrenamiento, salida = pickle.load(archivoPickle)
except:
    palabras=[]
    tags=[]
    auxX=[]
    auxY=[]

    for contenido in datos["contenido"]:
        for patrones in contenido["patrones"]:
            auxPalabra = nltk.word_tokenize(patrones)#para separar la frase
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(contenido["tag"])

            #si no esta agregado a la lista se adiciona
            if contenido["tag"] not in tags:
                tags.append(contenido["tag"])

    palabras = [stemmer.stem(w.lower()) for w in palabras if w !="?"]
    palabras = sorted(list(set(palabras)))
    tags = sorted(tags)

    entrenamiento = []
    salida = []

    salidaVacia = [0 for _ in range(len(tags))]

    #para asignarle un indice a cada palabra
    for x, documento in enumerate(auxX):
        cubeta = []
        auxPalabra = [stemmer.stem(w.lower()) for w in documento]
        for w in palabras:
            if w in auxPalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)
        filaSalida = salidaVacia[:]
        filaSalida[tags.index(auxY[x])] = 1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)

    #convertir una lista a un array
    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)
    with open("variables.pickle", "wb") as archivoPickle:
        pickle.dump((palabras, tags, entrenamiento, salida), archivoPickle)


#Crear la red neuronal en blanco
tensorflow.compat.v1.reset_default_graph()

red = tflearn.input_data(shape=[None, len(entrenamiento[0])])
red = tflearn.fully_connected(red,15)
red = tflearn.fully_connected(red,15)
red = tflearn.fully_connected(red, len(salida[0]), activation="softmax")
red = tflearn.regression(red)

modelo = tflearn.DNN(red)

#batch se debe agregar la cantidad que tenemos de patrones
modelo.fit(entrenamiento, salida, n_epoch=3000, batch_size=15, show_metric=True)
modelo.save("modelo.tflearn")

nombreBot = "FastFoods"

def obtenerRespuesta(entrada):
    #while True:
      #  entrada = input("Tu: ")
    cubeta = [0 for _ in range(len(palabras))]
    entradaProcesada = nltk.word_tokenize(entrada)
    entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
    for palabraIndividual in entradaProcesada:
        for i, palabra in enumerate(palabras):
            if palabra == palabraIndividual:
                cubeta[i] = 1
    resultados = modelo.predict([numpy.array(cubeta)])
    resultadosIndices = numpy.argmax(resultados)
    tag = tags[resultadosIndices]

    for tagAux in datos["contenido"]:
        if tagAux["tag"] == tag:
            return random.choice(tagAux["respuestas"])


    return "No te entendi..."


