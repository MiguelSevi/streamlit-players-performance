import pandas as pd
import sqlite3

# Cargar CSVs
performance_df = pd.read_csv("data/Performance_Stats.csv")
competitions_df = pd.read_csv("data/Competitions.csv")
general_df = pd.read_csv("data/General_Data.csv")
players_df = pd.read_csv("data/players_data.csv")

# Conectar o crear base de datos SQLite
conn = sqlite3.connect("database.db")

# Guardar DataFrames como tablas
performance_df.to_sql("performance_stats", conn, if_exists="replace", index=False)
competitions_df.to_sql("competitions", conn, if_exists="replace", index=False)
general_df.to_sql("general_data", conn, if_exists="replace", index=False)
players_df.to_sql("players_data", conn, if_exists="replace", index=False)

# Cerrar conexión
conn.close()

print("✅ Base de datos creada correctamente.")
