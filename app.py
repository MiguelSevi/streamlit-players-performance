
import streamlit as st
from pages.home import home
from pages.performance import performance
from pages.login import login


# Control de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    st.sidebar.title("Menú")
    pagina = st.sidebar.radio("Ir a:", ["Home", "Performance"])

    if pagina == "Home":
        home()
    elif pagina == "Performance":
        performance()
