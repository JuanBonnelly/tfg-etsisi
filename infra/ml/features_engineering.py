import os

import numpy as np
import pandas as pd
from tqdm import tqdm


df = pd.read_csv("data/dataset_partidos.csv", parse_dates=["fecha"])
df.sort_values(by="fecha", inplace=True)
df.reset_index(drop=True, inplace=True)

estadisticas = [
    "posesion_local", "posesion_visitante",
    "corners_local", "corners_visitante",
    "tarjetas_amarillas_local", "tarjetas_amarillas_visitante",
    "tarjetas_rojas_local", "tarjetas_rojas_visitante"
]

def _valor_equipo_en_partido(partido_row, equipo, var_base):
    """Devuelve el valor de una estadistica para un equipo en un partido"""

    if partido_row["nombre_equipo_local"] == equipo:
        return partido_row[f"{var_base}_local"]
    if partido_row["nombre_equipo_visitante"] == equipo:
        return partido_row[f"{var_base}_visitante"]
    return np.nan

def _media_diferencia_goles(partidos, equipo):
    """Calcula la diferencia media de goles de un equipo."""

    valores = []

    for _, partido in partidos.iterrows():
        if partido["nombre_equipo_local"] == equipo:
            valores.append(partido["goles_local"] - partido["goles_visitante"])
        elif partido["nombre_equipo_visitante"] == equipo:
            valores.append(partido["goles_visitante"] - partido["goles_local"])

    return np.mean(valores) if valores else np.nan

def _contar_victorias(partidos, equipo):
    """Cuenta las victorias de un equipo en varios partidos."""
    count = 0

    for _, partido in partidos.iterrows():
        if partido["resultado"] == 1 and partido["nombre_equipo_local"] == equipo:
            count += 1
        elif partido["resultado"] == -1 and partido["nombre_equipo_visitante"] == equipo:
            count += 1

    return count


def _contar_empates(partidos, equipo):
    """Cuenta los empates de un equipo en varios partidos."""
    count = 0

    for _, partido in partidos.iterrows():
        if partido["resultado"] == 0 and (
            partido["nombre_equipo_local"] == equipo or partido["nombre_equipo_visitante"] == equipo
        ):
            count += 1

    return count


def _contar_derrotas(partidos, equipo):
    """Cuenta las derrotas de un equipo en varios partidos."""
    count = 0

    for _, partido in partidos.iterrows():
        if partido["resultado"] == -1 and partido["nombre_equipo_local"] == equipo:
            count += 1
        elif partido["resultado"] == 1 and partido["nombre_equipo_visitante"] == equipo:
            count += 1

    return count


# Primera fase: Se obtiene las medias de los ultimos 10 partidos de un equipo
for var in estadisticas:
    df[f"media_ult10_{var}"] = np.nan  

for i, row in tqdm(df.iterrows(), total=len(df)):
    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]
    ultimos_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)
    ultimos_visitante = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)
    for var in estadisticas:
        var_base = var.replace("_local", "").replace("_visitante", "")
        if "local" in var:
            valores = ultimos_local.apply(lambda r: _valor_equipo_en_partido(r, equipo_local, var_base), axis=1).dropna()
        else:
            valores = ultimos_visitante.apply(lambda r: _valor_equipo_en_partido(r, equipo_visitante, var_base), axis=1).dropna()
        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_ult10_{var}"] = media

# Segunda fase: Se añade las medias de los ultimos enfrentamientos directos (H2H)
h2h_vars = estadisticas  
df["tendencia_empate_h2h"] = np.nan

for var in h2h_vars:
    df[f"media_h2h_{var}"] = np.nan

for i, row in tqdm(df.iterrows(), total=len(df), desc="H2H"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    enfrentamientos = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    for var in h2h_vars:
        var_base = var.replace("_local", "").replace("_visitante", "")
        if "local" in var:
            valores = enfrentamientos.apply(lambda r: _valor_equipo_en_partido(r, equipo_local, var_base), axis=1).dropna()
        else:
            valores = enfrentamientos.apply(lambda r: _valor_equipo_en_partido(r, equipo_visitante, var_base), axis=1).dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_h2h_{var}"] = media

    if not enfrentamientos.empty:
        empates_h2h = (enfrentamientos["resultado"] == 0).sum()
        df.at[i, "tendencia_empate_h2h"] = empates_h2h / len(enfrentamientos)
    else:
        df.at[i, "tendencia_empate_h2h"] = np.nan

# Tercera fase: Se añade las medias historicas acumuladas de cada equipo
for var in estadisticas:
    df[f"media_hist_{var}"] = np.nan

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
        var_base = var.replace("_local", "").replace("_visitante", "")

        if "local" in var:
            valores = partidos_local.apply(lambda r: _valor_equipo_en_partido(r, equipo_local, var_base), axis=1).dropna()
        else:
            valores = partidos_visitante.apply(lambda r: _valor_equipo_en_partido(r, equipo_visitante, var_base), axis=1).dropna()

        media = valores.mean() if not valores.empty else np.nan
        df.at[i, f"media_hist_{var}"] = media

# Cuarta fase: Se obtiene la diferencia media de goles

for prefijo in ["media_ult10", "media_h2h", "media_hist"]:
    df[f"{prefijo}_diferencia_goles_local"] = np.nan
    df[f"{prefijo}_diferencia_goles_visitante"] = np.nan

for i, row in tqdm(df.iterrows(), total=len(df), desc="Diferencia Goles"):
    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    ult_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) 
        & (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    ult_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) 
                & (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)


    df.at[i, "media_ult10_diferencia_goles_local"] = _media_diferencia_goles(ult_local, equipo_local)
    df.at[i, "media_ult10_diferencia_goles_visitante"] = _media_diferencia_goles(ult_visit, equipo_visitante)

    h2h = df[
        (
            ((df["nombre_equipo_local"] == equipo_local) & (df["nombre_equipo_visitante"] == equipo_visitante)) |
            ((df["nombre_equipo_local"] == equipo_visitante) & (df["nombre_equipo_visitante"] == equipo_local))
        ) & (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(10)

    df.at[i, "media_h2h_diferencia_goles_local"] = _media_diferencia_goles(h2h, equipo_local)
    df.at[i, "media_h2h_diferencia_goles_visitante"] = _media_diferencia_goles(h2h, equipo_visitante)


    hist_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)]
    hist_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)]

    df.at[i, "media_hist_diferencia_goles_local"] = _media_diferencia_goles(hist_local, equipo_local)
    df.at[i, "media_hist_diferencia_goles_visitante"] = _media_diferencia_goles(hist_visit, equipo_visitante)

# Quinta fase: Se añade las rachas y diferencias de estadisticas  

df["racha_ganados_local_ult5"] = np.nan
df["racha_ganados_visitante_ult5"] = np.nan
df["diferencia_posesion"] = df["media_ult10_posesion_local"] - df["media_ult10_posesion_visitante"]
df["diferencia_corners"] = df["media_ult10_corners_local"] - df["media_ult10_corners_visitante"]
df["diferencia_tarjetas_amarillas"] = df["media_ult10_tarjetas_amarillas_local"] - df["media_ult10_tarjetas_amarillas_visitante"]
df["diferencia_tarjetas_rojas"] = df["media_ult10_tarjetas_rojas_local"] - df["media_ult10_tarjetas_rojas_visitante"]
df["media_hist_goles_local_a_favor"] = np.nan
df["media_hist_goles_local_en_contra"] = np.nan
df["racha_empates_local_ult5"] = np.nan
df["racha_derrotas_local_ult5"] = np.nan
df["racha_empates_visitante_ult5"] = np.nan
df["racha_derrotas_visitante_ult5"] = np.nan
df["goles_local_ult5_media"] = np.nan
df["goles_visitante_ult5_media"] = np.nan
df["tendencia_empate_local"] = np.nan
df["tendencia_empate_visitante"] = np.nan

for i, row in tqdm(df.iterrows(), total=len(df), desc="Rachas y diferencias"):

    fecha_actual = row["fecha"]
    equipo_local = row["nombre_equipo_local"]
    equipo_visitante = row["nombre_equipo_visitante"]

    ult5_local = df[
        ((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(5)

    ult5_visit = df[
        ((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) &
        (df["fecha"] < fecha_actual)
    ].sort_values(by="fecha", ascending=False).head(5)

    df.at[i, "racha_ganados_local_ult5"] = _contar_victorias(ult5_local, equipo_local)
    df.at[i, "racha_ganados_visitante_ult5"] = _contar_victorias(ult5_visit, equipo_visitante)
    df.at[i, "racha_empates_local_ult5"] = _contar_empates(ult5_local, equipo_local)
    df.at[i, "racha_derrotas_local_ult5"] = _contar_derrotas(ult5_local, equipo_local)
    df.at[i, "racha_empates_visitante_ult5"] = _contar_empates(ult5_visit, equipo_visitante)
    df.at[i, "racha_derrotas_visitante_ult5"] = _contar_derrotas(ult5_visit, equipo_visitante)
    
    partidos_local_en_casa = df[
        (df["nombre_equipo_local"] == equipo_local) & (df["fecha"] < fecha_actual)
    ]
    df.at[i, "media_hist_goles_local_a_favor"] = partidos_local_en_casa["goles_local"].mean() if not partidos_local_en_casa.empty else np.nan
    df.at[i, "media_hist_goles_local_en_contra"] = partidos_local_en_casa["goles_visitante"].mean() if not partidos_local_en_casa.empty else np.nan

    df.at[i, "goles_local_ult5_media"] = ult5_local.apply(
        lambda p: p["goles_local"] if p["nombre_equipo_local"] == equipo_local else p["goles_visitante"],
        axis=1
    ).mean()
    
    df.at[i, "goles_visitante_ult5_media"] = ult5_visit.apply(
        lambda p: p["goles_visitante"] if p["nombre_equipo_visitante"] == equipo_visitante else p["goles_local"],
        axis=1
    ).mean()

    ult10_local = df[((df["nombre_equipo_local"] == equipo_local) | (df["nombre_equipo_visitante"] == equipo_local)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)
    ult10_visit = df[((df["nombre_equipo_local"] == equipo_visitante) | (df["nombre_equipo_visitante"] == equipo_visitante)) & (df["fecha"] < fecha_actual)].sort_values(by="fecha", ascending=False).head(10)

    empate_local = (ult10_local["resultado"] == 0).sum()
    empate_visit = (ult10_visit["resultado"] == 0).sum()

    df.at[i, "tendencia_empate_local"] = empate_local / len(ult10_local) if len(ult10_local) > 0 else np.nan
    df.at[i, "tendencia_empate_visitante"] = empate_visit / len(ult10_visit) if len(ult10_visit) > 0 else np.nan

# Guardado final del nuevo dataset enriquecido
os.makedirs("data", exist_ok=True)
df.to_csv("data/dataset_partidos_enriquecido.csv", index=False)
print("Dataset enriquecido guardado como 'data/dataset_partidos_enriquecido.csv'")
