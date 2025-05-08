import streamlit as st
import requests
import time
import uuid
from PIL import Image
import io

# Título de la aplicación
st.title("Generador de Imágenes con IA")

# Generar un session_id único
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# Inicializar el historial de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar el historial de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["type"] == "text":
            st.markdown(message["content"])
        elif message["type"] == "image":
            st.image(message["content"], caption=message.get("caption", ""))

# Función para obtener imagen desde URL
def get_image_from_url(url):
    response = requests.get(url)
    image = Image.open(io.BytesIO(response.content))
    return image

# Entrada del usuario
if prompt := st.chat_input("Describe la imagen que quieres generar:", disabled=st.session_state.get("loading", False)):
    # Agregar la pregunta del usuario al historial
    st.session_state.messages.append({"role": "user", "type": "text", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Mostrar spinner y deshabilitar el input
    st.session_state.loading = True
    
    # Llamar a la API de generación de imágenes
    with st.spinner("Generando imagen..."):
        try:
            response = requests.post(
                "http://20.94.168.174/api/image-generation",
                json={
                    "prompt": prompt,
                    "session_id": st.session_state.session_id
                }
            )
            
            if response.status_code == 200:
                response_data = response.json()
                image_url_1 = response_data.get("image_url_1", "")
                image_url_2 = response_data.get("image_url_2", "")
                
                if image_url_1 or image_url_2:
                    with st.chat_message("assistant"):
                        # Usar columnas para mostrar imágenes horizontalmente
                        if image_url_1 and image_url_2:
                            col1, col2 = st.columns(2)
                            # Mostrar imagen de gpt-image-1
                            with col1:
                                image1 = get_image_from_url(image_url_1)
                                st.image(image1, caption="gpt-image-1")
                                # Agregar la imagen al historial
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "type": "image", 
                                    "content": image1,
                                    "caption": "gpt-image-1"
                                })
                            
                            # Mostrar imagen de Dall-e3
                            with col2:
                                image2 = get_image_from_url(image_url_2)
                                st.image(image2, caption="Dall-e3")
                                # Agregar la imagen al historial
                                st.session_state.messages.append({
                                    "role": "assistant", 
                                    "type": "image", 
                                    "content": image2,
                                    "caption": "Dall-e3"
                                })
                        elif image_url_1:
                            # Solo mostrar imagen de gpt-image-1
                            image1 = get_image_from_url(image_url_1)
                            st.image(image1, caption="gpt-image-1")
                            # Agregar la imagen al historial
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "type": "image", 
                                "content": image1,
                                "caption": "gpt-image-1"
                            })
                        elif image_url_2:
                            # Solo mostrar imagen de Dall-e3
                            image2 = get_image_from_url(image_url_2)
                            st.image(image2, caption="Dall-e3")
                            # Agregar la imagen al historial
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "type": "image", 
                                "content": image2,
                                "caption": "Dall-e3"
                            })
                else:
                    error_msg = "La API no devolvió URLs de imágenes válidas."
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "type": "text", 
                        "content": error_msg
                    })
                    with st.chat_message("assistant"):
                        st.markdown(error_msg)
            else:
                error_msg = f"Error en la API: Código {response.status_code}"
                st.session_state.messages.append({
                    "role": "assistant", 
                    "type": "text", 
                    "content": error_msg
                })
                with st.chat_message("assistant"):
                    st.markdown(error_msg)
                    
        except Exception as e:
            error_msg = f"Error al conectar con la API: {str(e)}"
            st.session_state.messages.append({
                "role": "assistant", 
                "type": "text", 
                "content": error_msg
            })
            with st.chat_message("assistant"):
                st.markdown(error_msg)
    
    # Habilitar el input nuevamente
    st.session_state.loading = False
    st.rerun()  # Esto ayuda a actualizar el estado del chat_input