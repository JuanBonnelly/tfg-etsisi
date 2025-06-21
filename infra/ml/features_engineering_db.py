# infra/ml/features_engineering_db.py
import sys
import os
# Asegúrate de que estas rutas son correctas para importar desde la raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import pandas as pd
import numpy as np
from datetime import date
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

# Importa tus componentes del backend que estás probando
from infra.database.mysql_connect import get_session # Para obtener una sesión de DB
from backend.repositories.team_repository import TeamRepository
from backend.repositories.partido_repository import PartidoRepository
from backend.services.prediction_service import PredictionService # ¡La clase que estamos desarrollando!

# --- Función auxiliar para el cálculo de features (adaptadas de tu features_engineering.py) ---
# Estas funciones son similares a las que ya he puesto dentro de PredictionService,
# pero las mantenemos aquí en el laboratorio para que puedas ver el proceso.
# La idea es que _calculate_features_for_single_match en PredictionService
# las use o tenga lógica equivalente.

def _get_match_result(partido_data: Dict[str, Any]) -> int:
    """Calcula el resultado (1:victoria, 0:empate, -1:derrota) desde el punto de vista del equipo en cuestión."""
    if partido_data["goles_a_favor"] == partido_data["goles_en_contra"]:
        return 0  # Empate
    return 1 if partido_data["goles_a_favor"] > partido_data["goles_en_contra"] else -1

def _calculate_average_stats(data: List[Dict[str, Any]], stat_key: str) -> float:
    """Calcula la media de una estadística de una lista de diccionarios de partidos."""
    values = [d[stat_key] for d in data if d.get(stat_key) is not None and not np.isnan(d[stat_key])]
    return np.mean(values) if values else np.nan

def _calculate_avg_goal_diff(data: List[Dict[str, Any]]) -> float:
    """Calcula la media de la diferencia de goles para un equipo en una lista de partidos."""
    difs = [d["goles_a_favor"] - d["goles_en_contra"] for d in data if d.get("goles_a_favor") is not None and d.get("goles_en_contra") is not None]
    return np.mean(difs) if difs else np.nan

def _calculate_racha(data: List[Dict[str, Any]], result_type: int) -> int:
    """Calcula la racha de victorias, empates o derrotas en una lista de partidos."""
    count = 0
    for d in data:
        if d.get("resultado") is not None and d["resultado"] == result_type:
            count += 1
        else:
            break # La racha se rompe si el resultado no es el esperado
    return count

# --- Script de Prueba ---
def test_prediction_features_from_db():
    session: Optional[Session] = None
    try:
        session = get_session()
        prediction_service = PredictionService(session)
        team_repo = TeamRepository(session)

        # --- DATOS DE PRUEBA ---
        # Asegúrate de que estos equipos existan en tu DB 'futbol_TFG' y tengan historial.
        # Puedes usar el script testprueba.py para cargar datos si no los tienes.
        local_team_name = "Arsenal"
        visitor_team_name = "Tottenham"
        prediction_date = date(2024, 6, 18) # Una fecha actual o futura para la predicción

        # Obtener IDs de equipos
        local_team = team_repo.get_team_by_name(local_team_name)
        visitor_team = team_repo.get_team_by_name(visitor_team_name)

        if not local_team or not visitor_team:
            print(f"Error: Uno o ambos equipos no encontrados. Local: {local_team_name}, Visitante: {visitor_team_name}")
            print("Asegúrate de que tienes datos en la DB 'futbol_TFG' y que los nombres coinciden.")
            return

        local_team_id = local_team.equipo_id
        visitor_team_id = visitor_team.equipo_id

        print(f"\n--- Calculando features para {local_team_name} vs {visitor_team_name} el {prediction_date} ---")

        # Llama a la función que calcula las features (¡la que estás desarrollando en PredictionService!)
        features_df = prediction_service._calculate_features_for_single_match(
            local_team_id, visitor_team_id, prediction_date
        )

        if features_df is None or features_df.empty:
            print("No se pudieron generar features. Revisa los datos históricos o la lógica de _calculate_features_for_single_match.")
            return

        print("\n--- DataFrame de Features Calculadas ---")
        print(features_df.head())

        print(f"\n--- Valores de Features Individuales (Verifica NaNs) ---")
        for col in PredictionService._MODEL_FEATURES:
            value = features_df[col].iloc[0]
            print(f"{col}: {value} (Tipo: {type(value).__name__})")

        # Opcional: Comparar con tu dataset_partidos_enriquecido.csv si tienes un partido similar
        # df_enriched = pd.read_csv("data/dataset_partidos_enriquecido.csv", parse_dates=["fecha"])
        # df_sample = df_enriched[(df_enriched["nombre_equipo_local"] == local_team_name) &
        #                         (df_enriched["nombre_equipo_visitante"] == visitor_team_name) &
        #                         (df_enriched["fecha"] < prediction_date)].tail(1)
        # if not df_sample.empty:
        #     print("\n--- Comparación con Dataset Enriquecido ---")
        #     print(df_sample[PredictionService._MODEL_FEATURES].head())
        # else:
        #     print("\nNo se encontró un partido similar en el dataset enriquecido para comparar.")


    except Exception as e:
        print(f"\n¡Ocurrió un error inesperado durante la prueba! {e}")
        import traceback
        traceback.print_exc()
    finally:
        if session:
            session.close()

if __name__ == "__main__":
    test_prediction_features_from_db()