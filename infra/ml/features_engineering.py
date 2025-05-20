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

# ---------------SEGUNDA FASE: añadir medias de últimos 10 enfrentamientos directos----------------
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

# -------- TERCERA FASE: medias históricas acumuladas -----
for var in estadisticas:
    df[f"media_hist_{var}"] = np.nan

print(" Añadiendo medias históricas acumuladas por equipo...")

for i, row in tqdm(df.iterrows(), total=len(df), desc="Histórico"):
    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    partidos_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ]

    partidos_visitante = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ]

    for var in estadisticas:
        if "local" in var:
            valores = partidos_local[var].dropna()
        else:
            valores = partidos_visitante[var].dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_hist_{var}"] = media

# ----------------CUARTA FASE: diferencia de goles en todos los contextos---------------------
print(" Calculando diferencias de goles...")

# Añadir columnas vacías
for prefijo in ["media_ult10", "media_h2h", "media_hist"]:
    df[f"{prefijo}_diferencia_goles_local"] = np.nan
    df[f"{prefijo}_diferencia_goles_visitante"] = np.nan

for i, row in tqdm(df.iterrows(), total=len(df), desc="Diferencia Goles"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    # Últimos 10 partidos
    ult_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)
    ult_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)

    def diferencia(partidos, equipo):
        difs = []
        for _, p in partidos.iterrows():
            if p["nombre_equipo_local"] == equipo:
                difs.append(p["goles_local"] - p["goles_visitante"])
            elif p["nombre_equipo_visitante"] == equipo:
                difs.append(p["goles_visitante"] - p["goles_local"])
        return np.mean(difs) if difs else np.nan

    df.at[i, "media_ult10_diferencia_goles_local"] = diferencia(ult_local, equipo_local)
    df.at[i, "media_ult10_diferencia_goles_visitante"] = diferencia(ult_visit, equipo_visitante)

    # H2H
    h2h = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) & (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    df.at[i, "media_h2h_diferencia_goles_local"] = diferencia(h2h, equipo_local)
    df.at[i, "media_h2h_diferencia_goles_visitante"] = diferencia(h2h, equipo_visitante)

    # Históricos
    hist_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)]
    hist_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)]

    df.at[i, "media_hist_diferencia_goles_local"] = diferencia(hist_local, equipo_local)
    df.at[i, "media_hist_diferencia_goles_visitante"] = diferencia(hist_visit, equipo_visitante)


# Verificar columnas esperadas en el dataset enriquecido
columnas_esperadas = [
    "media_ult10_diferencia_goles_local", "media_ult10_diferencia_goles_visitante",
    "media_h2h_diferencia_goles_local", "media_h2h_diferencia_goles_visitante",
    "media_hist_diferencia_goles_local", "media_hist_diferencia_goles_visitante"
]

print("\n Verificando columnas de diferencia de goles...")
faltantes = [col for col in columnas_esperadas if col not in df.columns]

if not faltantes:
    print(" Todas las columnas de diferencia de goles están presentes.")
else:
    print(" Faltan columnas en el dataset:", faltantes)

# Opcional: mostrar valores de ejemplo
print("\n Ejemplo de diferencias de goles (primeros 3 partidos):")
print(df[["nombre_equipo_local", "nombre_equipo_visitante", "fecha"] + columnas_esperadas].head(3))

# Crear carpeta de salida
os.makedirs("data", exist_ok=True)

# Guardar el nuevo dataset enriquecido
df.to_csv("data/dataset_partidos_enriquecido.csv", index=False)
print("Dataset enriquecido guardado como 'data/dataset_partidos_enriquecido.csv'")
