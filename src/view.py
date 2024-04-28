#Es necesario tener steamlit en el equipo
import streamlit as st
from controller_chatbot import predict_class, get_response, intents

st.title("🐉 Quetzal-Bot")

#Mostrar mensaje si es la primera vez que se ejecuta la aplicación web
if "messages" not in st.session_state:
    st.session_state.messages = []
if "first_message" not in st.session_state:
    st.session_state.first_message = True

#Mostrar histórico de mensajes, se recorre array de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Comprobar si se ejecuta por prinera vez el código
if st.session_state.first_message:
    with st.chat_message("assistant"):
        st.markdown("Bienvenidx upiicsianx!, ¿en qué puedo ayudarte?")

        #Se añade al array de mensajes
        st.session_state.messages.append({"role":"assistant", "content": "Hola, ¿en qué puedo ayudarte?"})
        st.session_state.first_message = False

#Crear el prompt para responder al usuario en función de lo que haya escrito
if prompt := st.chat_input("Escribe tu duda"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user","content": prompt})

    insts = predict_class(prompt)
    res = get_response(insts, intents)

    #Respuesta de chat 
    with st.chat_message("assistant"):
        st.markdown(res)
    st.session_state.messages.append({"role":"assistant", "content":res})



