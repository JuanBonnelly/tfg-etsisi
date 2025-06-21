# backend/services/prediction_service.py
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, Any, List, Optional, Tuple
from datetime import date
import traceback

from backend.repositories.partido_repository import PartidoRepository
from backend.repositories.team_repository import TeamRepository

class PredictionService:
    # --- LISTA DEFINITIVA Y CORRECTA OBTENIDA DEL SCALER ---
    _MODEL_FEATURES = [
        'media_ult10_posesion_local', 'media_ult10_posesion_visitante', 'media_ult10_corners_local',
        'media_ult10_corners_visitante', 'media_ult10_tarjetas_amarillas_local',
        'media_ult10_tarjetas_amarillas_visitante', 'media_ult10_tarjetas_rojas_local',
        'media_ult10_tarjetas_rojas_visitante', 'tendencia_empate_h2h', 'media_h2h_posesion_local',
        'media_h2h_posesion_visitante', 'media_h2h_corners_local', 'media_h2h_corners_visitante',
        'media_h2h_tarjetas_amarillas_local', 'media_h2h_tarjetas_amarillas_visitante',
        'media_h2h_tarjetas_rojas_local', 'media_h2h_tarjetas_rojas_visitante',
        'media_hist_posesion_local', 'media_hist_posesion_visitante', 'media_hist_corners_local',
        'media_hist_corners_visitante', 'media_hist_tarjetas_amarillas_local',
        'media_hist_tarjetas_amarillas_visitante', 'media_hist_tarjetas_rojas_local',
        'media_hist_tarjetas_rojas_visitante', 'media_ult10_diferencia_goles_local',
        'media_ult10_diferencia_goles_visitante', 'media_h2h_diferencia_goles_local',
        'media_h2h_diferencia_goles_visitante', 'media_hist_diferencia_goles_local',
        'media_hist_diferencia_goles_visitante', 'racha_ganados_local_ult5',
        'racha_ganados_visitante_ult5', 'diferencia_posesion', 'diferencia_corners',
        'diferencia_tarjetas_amarillas', 'diferencia_tarjetas_rojas',
        'media_hist_goles_local_a_favor', 'media_hist_goles_local_en_contra',
        'racha_empates_local_ult5', 'racha_derrotas_local_ult5', 'racha_empates_visitante_ult5',
        'racha_derrotas_visitante_ult5', 'tendencia_empate_local', 'tendencia_empate_visitante'
    ]

    def __init__(self, db_session: Session):
        self.partido_repo = PartidoRepository(db_session)
        self.team_repo = TeamRepository(db_session)

    def _get_match_result(self, partido: Any, team_id: str) -> int:
        if partido.goles_local is None or partido.goles_visitante is None: return 0
        if partido.goles_local == partido.goles_visitante: return 0
        if partido.equipo_local_id == team_id:
            return 1 if partido.goles_local > partido.goles_visitante else -1
        else:
            return 1 if partido.goles_visitante > partido.goles_local else -1

    def _calculate_team_match_stats(self, partido: Any, stats: Any, team_id: str) -> Dict[str, Any]:
        is_local = (partido.equipo_local_id == team_id)
        base_stats = {
            "goles_a_favor": partido.goles_local if is_local else partido.goles_visitante,
            "goles_en_contra": partido.goles_visitante if is_local else partido.goles_local,
            "es_local": is_local, "resultado": self._get_match_result(partido, team_id)
        }
        if not stats:
            base_stats.update({"posesion": np.nan, "corners": np.nan, "tarjetas_amarillas": np.nan, "tarjetas_rojas": np.nan})
        else:
            base_stats.update({
                "posesion": stats.posesion_local if is_local else stats.posesion_visitante,
                "corners": stats.corners_local if is_local else stats.corners_visitante,
                "tarjetas_amarillas": stats.tarjetas_amarillas_local if is_local else stats.tarjetas_amarillas_visitante,
                "tarjetas_rojas": stats.tarjetas_rojas_local if is_local else stats.tarjetas_rojas_visitante
            })
        return base_stats

    def _get_team_historical_data(self, team_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        matches_with_stats = self.partido_repo.get_historical_matches_with_stats(team_id, match_date, limit=limit)
        return [self._calculate_team_match_stats(p, s, team_id) for p, s in matches_with_stats]

    def _get_h2h_historical_data(self, team1_id: str, team2_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        matches_with_stats = self.partido_repo.get_h2h_matches_with_stats(team1_id, team2_id, match_date, limit=limit)
        processed_data = []
        for partido, stats in matches_with_stats:
            data_point = {
                "local_goles": partido.goles_local, "visitor_goles": partido.goles_visitante,
                "resultado_local_perspective": self._get_match_result(partido, team1_id)
            }
            if stats:
                data_point.update({
                    "local_posesion": stats.posesion_local, "visitor_posesion": stats.posesion_visitante,
                    "local_corners": stats.corners_local, "visitor_corners": stats.corners_visitante,
                    "local_tarjetas_amarillas": stats.tarjetas_amarillas_local, "visitor_tarjetas_amarillas": stats.tarjetas_amarillas_visitante,
                    "local_tarjetas_rojas": stats.tarjetas_rojas_local, "visitor_tarjetas_rojas": stats.tarjetas_rojas_visitante
                })
            processed_data.append(data_point)
        return processed_data

    def _calculate_average_stats(self, data: List[Dict[str, Any]], stat_key: str) -> float:
        values = [d[stat_key] for d in data if d.get(stat_key) is not None and not np.isnan(d[stat_key])]
        return np.mean(values) if values else np.nan

    def _calculate_features_for_single_match(self, local_team_id: str, visitor_team_id: str, match_date: date) -> pd.DataFrame:
        features = {}
        
        local_ult10_data = self._get_team_historical_data(local_team_id, match_date, limit=10)
        visitor_ult10_data = self._get_team_historical_data(visitor_team_id, match_date, limit=10)
        if not local_ult10_data or not visitor_ult10_data:
            raise ValueError("Datos históricos insuficientes (ult10) para generar predicción.")

        h2h_data = self._get_h2h_historical_data(local_team_id, visitor_team_id, match_date, limit=10)
        local_hist_data = self._get_team_historical_data(local_team_id, match_date)
        visitor_hist_data = self._get_team_historical_data(visitor_team_id, match_date)
        local_ult5_data = local_ult10_data[:5]
        visitor_ult5_data = visitor_ult10_data[:5]

        for stat in ["posesion", "corners", "tarjetas_amarillas", "tarjetas_rojas"]:
            features[f"media_ult10_{stat}_local"] = self._calculate_average_stats(local_ult10_data, stat)
            features[f"media_ult10_{stat}_visitante"] = self._calculate_average_stats(visitor_ult10_data, stat)
            features[f"media_hist_{stat}_local"] = self._calculate_average_stats(local_hist_data, stat)
            features[f"media_hist_{stat}_visitante"] = self._calculate_average_stats(visitor_hist_data, stat)
            
            local_avg_h2h, visitor_avg_h2h = np.nan, np.nan
            if h2h_data:
                local_vals = [d.get(f"local_{stat}") for d in h2h_data if d.get(f"local_{stat}") is not None]
                visitor_vals = [d.get(f"visitor_{stat}") for d in h2h_data if d.get(f"visitor_{stat}") is not None]
                if local_vals: local_avg_h2h = np.mean(local_vals)
                if visitor_vals: visitor_avg_h2h = np.mean(visitor_vals)
            features[f"media_h2h_{stat}_local"] = local_avg_h2h
            features[f"media_h2h_{stat}_visitante"] = visitor_avg_h2h

        features["tendencia_empate_h2h"] = np.mean([1 for d in h2h_data if d.get("resultado_local_perspective") == 0]) if h2h_data else np.nan
        features["media_ult10_diferencia_goles_local"] = self._calculate_average_stats(local_ult10_data, "goles_a_favor") - self._calculate_average_stats(local_ult10_data, "goles_en_contra")
        features["media_ult10_diferencia_goles_visitante"] = self._calculate_average_stats(visitor_ult10_data, "goles_a_favor") - self._calculate_average_stats(visitor_ult10_data, "goles_en_contra")
        h2h_diffs_local = [d["local_goles"] - d["visitor_goles"] for d in h2h_data if d.get("local_goles") is not None and d.get("visitor_goles") is not None]
        features["media_h2h_diferencia_goles_local"] = np.mean(h2h_diffs_local) if h2h_diffs_local else np.nan
        features["media_h2h_diferencia_goles_visitante"] = -features.get("media_h2h_diferencia_goles_local", np.nan)
        features["media_hist_diferencia_goles_local"] = self._calculate_average_stats(local_hist_data, "goles_a_favor") - self._calculate_average_stats(local_hist_data, "goles_en_contra")
        features["media_hist_diferencia_goles_visitante"] = self._calculate_average_stats(visitor_hist_data, "goles_a_favor") - self._calculate_average_stats(visitor_hist_data, "goles_en_contra")

        for r_type, r_name in zip([1, 0, -1], ["ganados", "empates", "derrotas"]):
            features[f"racha_{r_name}_local_ult5"] = sum(1 for d in local_ult5_data if d.get("resultado") == r_type)
            features[f"racha_{r_name}_visitante_ult5"] = sum(1 for d in visitor_ult5_data if d.get("resultado") == r_type)

        features["diferencia_posesion"] = features.get("media_ult10_posesion_local", 0) - features.get("media_ult10_posesion_visitante", 0)
        features["diferencia_corners"] = features.get("media_ult10_corners_local", 0) - features.get("media_ult10_corners_visitante", 0)
        features["diferencia_tarjetas_amarillas"] = features.get("media_ult10_tarjetas_amarillas_local", 0) - features.get("media_ult10_tarjetas_amarillas_visitante", 0)
        features["diferencia_tarjetas_rojas"] = features.get("media_ult10_tarjetas_rojas_local", 0) - features.get("media_ult10_tarjetas_rojas_visitante", 0)
        
        local_home_matches = [d for d in local_hist_data if d.get("es_local")]
        features["media_hist_goles_local_a_favor"] = self._calculate_average_stats(local_home_matches, "goles_a_favor")
        features["media_hist_goles_local_en_contra"] = self._calculate_average_stats(local_home_matches, "goles_en_contra")
        
        features["tendencia_empate_local"] = np.mean([1 for d in local_ult10_data if d.get("resultado") == 0]) if local_ult10_data else 0.0
        features["tendencia_empate_visitante"] = np.mean([1 for d in visitor_ult10_data if d.get("resultado") == 0]) if visitor_ult10_data else 0.0
        
        features_df = pd.DataFrame([features])
        reindexed_df = features_df.reindex(columns=self._MODEL_FEATURES)
        return reindexed_df.fillna(0)

    def predict_match_result(
        self, local_team_name: str, visitor_team_name: str, match_date: date,
        ml_model: RandomForestClassifier, scaler: StandardScaler
    ) -> Tuple[str, Dict[str, float]]:
        
        local_team = self.team_repo.get_team_by_name(local_team_name)
        if not local_team: raise ValueError(f"Equipo local '{local_team_name}' no encontrado.")
        
        visitor_team = self.team_repo.get_team_by_name(visitor_team_name)
        if not visitor_team: raise ValueError(f"Equipo visitante '{visitor_team_name}' no encontrado.")
        
        features_df = self._calculate_features_for_single_match(local_team.equipo_id, visitor_team.equipo_id, match_date)
        
        features_scaled = scaler.transform(features_df)
        
        predicted_class_int = ml_model.predict(features_scaled)[0]
        probabilities = ml_model.predict_proba(features_scaled)[0]
        
        result_map = {1: "Victoria Local", 0: "Empate", -1: "Victoria Visitante"}
        predicted_result_str = result_map.get(int(predicted_class_int), "Desconocido")
        
        class_order = ml_model.classes_
        prob_dict = {result_map.get(int(label)): prob for label, prob in zip(class_order, probabilities)}
        
        final_probs = {
            "Victoria Local": prob_dict.get("Victoria Local", 0.0),
            "Empate": prob_dict.get("Empate", 0.0),
            "Victoria Visitante": prob_dict.get("Victoria Visitante", 0.0)
        }
        return predicted_result_str, final_probs