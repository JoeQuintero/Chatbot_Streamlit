import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
import os
from tensorflow import keras
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
#Obtener el directorio del archivo actual
current_dir = os.path.dirname(os.path.abspath(__file__))
#Construir la ruta del directorio del archivo actual
file_path = os.path.join(current_dir, 'intents.json')
words_path = os.path.join(current_dir, 'words.pkl')
classes_path = os.path.join(current_dir, 'classes.pkl')
model_path = os.path.join(current_dir, 'chatbot_model.h5')

#Leer archivo json
with open(file_path, 'r', encoding='utf-8') as file:
    intents = json.load(file)

# Cargar los archivos pickle
words = pickle.load(open(words_path, 'rb'))
classes = pickle.load(open(classes_path, 'rb'))
# Cargar el modelo
model = tf.keras.models.load_model(model_path)
#model = tf.keras.models.load_model('/home/josequintero/Desktop/Quetzal-Bot/src/chatbot_model.h5')

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len (words) 
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)            

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    #Define un valor umbral que en muchos casos, es el punto de corte para determinar si una predicción es lo suficientemente confiable como para ser aceptada
    ERROR_THRESHOLD = 0.8
    results = [[i,r] for i, r in enumerate (res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "No puedo ayudarte con esa consulta"  # Manejo de caso donde intents_list está vacía
    
    responses = []
    
    for intent_info in intents_list:
        tag = intent_info['intent']
        
        # Buscar la intención correspondiente en intents_json
        for intent in intents_json['intents']:
            if intent['tag'] == tag:
                response = random.choice(intent['responses'])
                responses.append(response)
                break
    
    if responses:
        result = random.choice(responses)
    else:
        result = "No hay respuestas disponibles para estas intenciones"
    
    return result