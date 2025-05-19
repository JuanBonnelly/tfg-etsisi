import pandas as pd
import numpy as np
import os
from tqdm import tqdm

# Cargar el dataset original
df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])
df.sort_values(by="fecha", inplace=True)
df.reset_index(drop=True, inplace=True)

# Columnas estadísticas a promediar
estadisticas = [
    "posesion_local", "posesion_visitante",
    "corners_local", "corners_visitante",
    "tarjetas_amarillas_local", "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local", "tarjetas_rojas_visitante"
]

# Crear nuevas columnas para las medias
for var in estadisticas:
    df[f"media_ult10_{var}"] = np.nan  # se rellenarán después

# Recorremos cada partido para calcular las medias históricas
for i, row in tqdm(df.iterrows(), total=len(df)):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Partidos anteriores del equipo local
    ultimos_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Partidos anteriores del equipo visitante
    ultimos_visitante = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Pruebas que funciona correctamente 
    if equipo_local == "Arsenal" and equipo_visitante == "Tottenham":
        print(fecha_actual)
        print("Últimos 10 Arsenal:", ultimos_local[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])
        print("Últimos 10 Tottenham:", ultimos_visitante[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])

    # Calcular medias para cada variable
    for var in estadisticas:
        if "local" in var:
            valores = ultimos_local[var].dropna()
        else:
            valores = ultimos_visitante[var].dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_ult10_{var}"] = media

# SEGUNDA FASE: añadir medias de últimos 10 enfrentamientos directos
h2h_vars = estadisticas  # mismas estadísticas

# Crear nuevas columnas para enfrentamientos directos
for var in h2h_vars:
    df[f"media_h2h_{var}"] = np.nan

# Recorremos nuevamente para calcular enfrentamientos directos
for i, row in tqdm(df.iterrows(), total=len(df), desc="H2H"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Buscar últimos 10 enfrentamientos entre ambos equipos antes de la fecha actual
    enfrentamientos = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    # Pruebas que funciona correctamente
    if equipo_local == "Arsenal" and equipo_visitante == "Tottenham":
        print(fecha_actual)
        print("H2H Arsenal-Tottenham:", enfrentamientos[["fecha", "nombre_equipo_local", "nombre_equipo_visitante"]])
    
    # Calcular medias
    for var in h2h_vars:
        valores = enfrentamientos[var].dropna()
        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_h2h_{var}"] = media

# Crear carpeta de salida
os.makedirs("data", exist_ok=True)

# Guardar el nuevo dataset enriquecido
df.to_csv("data/dataset_partidos_enriquecido.csv", index=False)
print("Dataset enriquecido guardado como 'data/dataset_partidos_enriquecido.csv'")
