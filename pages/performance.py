import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi


@st.cache_data
def load_data():
    return pd.read_csv('data/df_players_Performance.csv')

def performance():
    st.title("Performance - Análisis de Rendimiento")
    st.markdown("""
    Esta aplicación interactiva carga datos de jugadores y presenta visualizaciones basadas en una BBDD  
    Compara el rendimiento de un jugador frente al promedio de su posición y muestra análisis visuales.
    """)

    data = load_data()

    # Sidebar - Filtros
    st.sidebar.header("Filtros")
    posiciones = data["Position"].dropna().unique()
    posicion_seleccionada = st.sidebar.selectbox("Selecciona posición:", posiciones)
    jugadores_disponibles = data[data["Position"] == posicion_seleccionada]["Player_Name"].unique()
    jugador_seleccionado = st.sidebar.selectbox("Selecciona jugador:", jugadores_disponibles)

    jugador_data = data[data["Player_Name"] == jugador_seleccionado].iloc[0]
    promedio_posicion = data[data["Position"] == posicion_seleccionada]

    # Radar
    st.header("Perfil de Rendimiento por Posición")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader(jugador_data["Player_Name"])
        st.image(jugador_data["Photo"], width=150)
        st.markdown(f"""
        - **Nacionalidad:** {jugador_data.get('Nationship', 'N/D')}
        - **Edad:** {jugador_data['Age']}
        - **Equipo:** {jugador_data['Team']}
        - **Competición:** {jugador_data['Competition']}
        - **Posición:** {jugador_data['Position']}
        - **Perfil:** {jugador_data['Profile_Main_Characteristic']}
        - **Valor de Mercado:** {jugador_data.get('Marke_Value_M')} M
        - **Partidos:** {jugador_data['Matches_Played']}
        - **Min.Jugados:** {jugador_data['Minutes']}
        - **Titular:** {jugador_data['Start_Line_UP_Percent']} %
        """)

    with col2:
        st.subheader("Jugador vs Promedio Posicional")
        radar_labels = [
            'Matches_Index', 'Conditional_Index', 'Goal_Involvement_Index',
            'Passing_Index', 'Technical_Skills_Index', 'Offensive_Index',
            'Defensive_Index', 'Performance_Index', 'xPerformance_Index', 'Scouting_Index'
        ]

        jugador_vals = [jugador_data[label] for label in radar_labels]
        promedio_vals = promedio_posicion[radar_labels].mean().tolist()
        max_val = max(jugador_vals + promedio_vals)
        jugador_norm = [v / max_val for v in jugador_vals] + [jugador_vals[0] / max_val]
        promedio_norm = [v / max_val for v in promedio_vals] + [promedio_vals[0] / max_val]
        angles = [n / float(len(radar_labels)) * 2 * pi for n in range(len(radar_labels))] + [0]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.plot(angles, jugador_norm, label="Jugador", linewidth=2, color="green")
        ax.fill(angles, jugador_norm, alpha=0.3, color="green")
        ax.plot(angles, promedio_norm, label="Promedio", linewidth=2, color="deepskyblue")
        ax.fill(angles, promedio_norm, alpha=0.2, color="deepskyblue")
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(radar_labels, fontsize=8)
        ax.set_yticklabels([])
        ax.set_title("Índices de Rendimiento", size=14, y=1.1)
        ax.legend(loc="upper right", bbox_to_anchor=(1.1, 1.1))
        st.pyplot(fig)

    # Tabla comparativa
    st.subheader("Comparación Numérica de Índices")
    tabla_comparativa = pd.DataFrame([jugador_vals, promedio_vals], columns=radar_labels, index=[jugador_data["Player_Name"], "Promedio"])
    st.dataframe(tabla_comparativa.style.format("{:.2f}"), use_container_width=True)

    # Descripciones
    st.markdown("### Descripción de los Índices")
    descripciones = {
        'Matches Index': "Participación e influencia en partidos jugados.",
        'Conditional index': "Desempeño fisico bajo condiciones específicas de juego.",
        'Goal Involment Index': "Participación directa e indirecta en goles.",
        'Passing Index': "Precisión y calidad de pases.",
        'Technical Skills Index': "Habilidad técnica general del jugador.",
        'Offensive Index': "Contribución ofensiva al equipo.",
        'Defensive index': "Desempeño en labores defensivas.",
        'Performance Index': "Valoración global del rendimiento.",
        'xPerformance Index': "Rendimiento esperado o Potencial según datos avanzados.",
        'Scouting Index': "Puntuación basada en criterios de scouting para su fichaje."
    }
    for indice, descripcion in descripciones.items():
        st.markdown(f"- **{indice}**: {descripcion}")
