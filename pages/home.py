import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os


def get_data(query):
    # Construir la ruta del archivo CSV
    file_path = os.path.join('data', query)
    print(f"Intentando leer el archivo en la ruta: {file_path}")  # Agregar depuración

    # Verificar si el archivo existe
    if os.path.exists(file_path):
        try:
            # Intentar leer el archivo CSV y devolver el DataFrame
            data = pd.read_csv(file_path)
            if data.empty:
                print(f"El archivo {query} está vacío.")
            return data
        except Exception as e:
            print(f"Error al leer el archivo CSV: {e}")
            return None
    else:
        print(f"Error: El archivo {query} no se encuentra en la carpeta 'data'.")
        return None


def home():
    st.title("🏠 Home - Análisis de Jugadores Jóvenes")

    st.markdown("""
    Bienvenido a la plataforma de análisis de jugadores jóvenes top.  
    Esta aplicación, desarrollada en Streamlit, permite explorar una muestra representativa de una base de datos extensa 
    con información detallada sobre el rendimiento, características y mercado de los jugadores.  
    A continuación, se muestra una tabla con los datos generales, seguida de visualizaciones clave para el análisis.
    """)

    # Mostrar tabla con datos generales
    st.subheader("📋 Datos Generales de los Jugadores")
    query = "general_data.csv"  # El nombre del archivo CSV en la carpeta 'data'
    data = get_data(query)

    # Verificar si data no es None antes de continuar
    if data is not None:
        st.write(f"Datos cargados correctamente. Tipo de datos: {type(data)}")  # Mostrar tipo de datos
        st.dataframe(data)

        # Visualizaciones generales
        st.header("📊 Visualizaciones Generales")

        # Verificar si la columna 'Age' existe
        if 'Age' in data.columns:
            st.subheader("Distribución de Edades")
            fig1, ax1 = plt.subplots(figsize=(10, 5))
            sns.histplot(data["Age"], bins=20, kde=True, ax=ax1, color='skyblue')
            ax1.set_xlabel("Edad")
            ax1.set_ylabel("Cantidad de Jugadores")
            st.pyplot(fig1)
        else:
            st.error("La columna 'Age' no se encuentra en los datos.")

        # Verificar si las columnas necesarias existen
        if 'Propietary_Team' in data.columns and 'Market_Value_M' in data.columns:
            st.subheader("Valor de Mercado Promedio por Equipo")
            team_values = data.groupby("Propietary_Team")["Market_Value_M"].mean().reset_index()
            fig2, ax2 = plt.subplots(figsize=(10, 5))
            sns.barplot(x="Propietary_Team", y="Market_Value_M", data=team_values, ax=ax2, palette='viridis')
            ax2.set_xlabel("Equipo")
            ax2.set_ylabel("Valor Promedio (M)")
            ax2.set_title("Promedio de Valor de Mercado por Equipo")
            ax2.tick_params(axis='x', rotation=90)
            st.pyplot(fig2)
        else:
            st.error("Las columnas 'Propietary_Team' o 'Market_Value_M' no se encuentran en los datos.")
    else:
        st.error("No se pudo cargar el archivo CSV. Verifica que el archivo exista y esté en el formato correcto.")


