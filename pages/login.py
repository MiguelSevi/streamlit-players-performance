import streamlit as st

def login():
    st.title("Login")

    USERNAME = "Sevi"
    PASSWORD = "Sevi"

    username_input = st.text_input("Nombre de usuario", key="username_input")
    password_input = st.text_input("Contraseña", type="password", key="password_input")

    if st.button("Iniciar sesión"):
        if username_input == USERNAME and password_input == PASSWORD:
            st.session_state.logged_in = True
            st.success("¡Inicio de sesión exitoso!")
        else:
            st.session_state.logged_in = False
            st.error("Credenciales incorrectas")
            

