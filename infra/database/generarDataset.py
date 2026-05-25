import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
from dotenv import load_dotenv

from infra.database.mysql_connect import get_engine  


load_dotenv()


engine = get_engine()

query = """
SELECT 
    p.partido_id,
    p.fecha,
    el.nombre AS nombre_equipo_local,
    ev.nombre AS nombre_equipo_visitante,
    p.goles_local,
    p.goles_visitante,
    ep.posesion_local,
    ep.posesion_visitante,
    ep.corners_local,
    ep.corners_visitante,
    ep.tarjetas_amarillas_local,
    ep.tarjetas_amarillas_visitante,
    ep.tarjetas_rojas_local,
    ep.tarjetas_rojas_visitante,
    t.temporada_id AS temporada,
    c.nombre AS competicion
FROM partido p
JOIN estadisticas_partido ep ON p.partido_id = ep.partido_id
JOIN equipo el ON p.equipo_local_id = el.equipo_id
JOIN equipo ev ON p.equipo_visitante_id = ev.equipo_id
JOIN temporada t ON p.temporada_id = t.temporada_id
JOIN competicion c ON p.competicion_id = c.competicion_id;
"""


def calcular_resultado(row):
    if row.goles_local > row.goles_visitante:
        return 1
    if row.goles_local < row.goles_visitante:
        return -1
    return 0


df = pd.read_sql(query, engine)
df["resultado"] = df.apply(calcular_resultado, axis=1)

df.drop_duplicates(subset="partido_id", keep="first", inplace=True)
df.sort_values(by="fecha", inplace=True)

os.makedirs("data", exist_ok=True)
df.to_csv("data/dataset_partidos.csv", index=False, encoding="utf-8")

print("Dataset generado correctamente en 'data/dataset_partidos.csv'")
