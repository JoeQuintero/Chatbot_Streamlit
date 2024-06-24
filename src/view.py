#Es necesario tener steamlit en el equipo
import streamlit as st
from controller_chatbot import predict_class, get_response, intents
from streamlit_option_menu import option_menu

#FRONT_END
#------------------------------------------------------------------------------------------------
# Encabezado personalizado
st.set_page_config(page_title="Quetzal-Bot", page_icon="🐉", layout="wide", initial_sidebar_state="expanded")

with open('/home/josequintero/Desktop/Quetzal-Bot/src/style.css') as f:
    css = f.read()

st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

st.sidebar.title("PÁGINAS OFICIALES")
#Botón de enlace para ir a un link 
##st.link_button("Ir a la página oficial de UPIICSA", "https://www.upiicsa.ipn.mx/")   
st.sidebar.page_link("https://www.upiicsa.ipn.mx/oferta-educativa/", label="Programas académicos", icon="🎓")   
st.sidebar.page_link("https://admision.ipn.mx/portal/index.html", label="Convocatoria", icon="🗓️")
st.sidebar.page_link("https://www.upiicsa.ipn.mx/conocenos/directorio-upiicsa.pdf", label="Contáctos", icon="📞")   
st.sidebar.page_link("https://www.upiicsa.ipn.mx/estudiantes/gestion-escolar.html", label="Gestión escolar", icon="🗂️")  
st.sidebar.page_link("https://www.google.com.mx/maps/place/UPIICSA+%E2%80%93+Unidad+Profesional+Interdisciplinaria+de+Ingenier%C3%ADa+y+Ciencias+Sociales+y+Administrativas+IPN/@19.395889,-99.0944224,17z/data=!3m1!4b1!4m6!3m5!1s0x85d1fc2e3efc321b:0xabf8454acb3a3a99!8m2!3d19.395884!4d-99.0918475!16s%2Fg%2F1223ql0w?entry=ttu", label="Ubicación", icon="📍")  
st.sidebar.page_link("https://www.upiicsa.ipn.mx/notiupiicsa.html", label="NOTIUPIICSA", icon="📰")  



st.title("🐉 QUETZAL-BOT")

# Agregar sección

#PROMPT
#------------------------------------------------------------------------------------------------

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




 



