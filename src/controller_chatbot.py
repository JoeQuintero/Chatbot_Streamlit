import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
from tensorflow import keras
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('/home/josequintero/Desktop/Quetzal-Bot/src/intents.json', 'r', encoding='utf-8').read())
words = pickle.load(open('/home/josequintero/Desktop/Quetzal-Bot/src/words.pkl', 'rb'))
classes = pickle.load(open('/home/josequintero/Desktop/Quetzal-Bot/src/classes.pkl', 'rb'))
model = tf.keras.models.load_model('/home/josequintero/Desktop/Quetzal-Bot/src/chatbot_model.h5')

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
    ERROR_THRESHOLD = 0.5
    results = [[i,r] for i, r in enumerate (res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent':classes[r[0]], 'probability':str(r[1])})
    return return_list

def get_response(intents_list, intents_json):
    if not intents_list:
        return "No hay intenciones disponibles"  # Manejo de caso donde intents_list está vacía
    
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