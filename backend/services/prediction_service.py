from datetime import date
from typing import Dict, Any, List, Optional, Tuple

import numpy as np
import pandas as pd
import shap
from sqlalchemy.orm import Session
from sklearn.neural_network import MLPClassifier

from backend.repositories.partido_repository import PartidoRepository
from backend.repositories.team_repository import TeamRepository


class PredictionService:
    _MODEL_FEATURES = [
        "posesion_local",
        "posesion_visitante",
        "corners_local",
        "corners_visitante",
        "tarjetas_amarillas_local",
        "tarjetas_amarillas_visitante",
        "tarjetas_rojas_local",
        "tarjetas_rojas_visitante",
        "media_ult10_posesion_local",
        "media_ult10_posesion_visitante",
        "media_ult10_corners_local",
        "media_ult10_corners_visitante",
        "media_ult10_tarjetas_amarillas_local",
        "media_ult10_tarjetas_amarillas_visitante",
        "media_ult10_tarjetas_rojas_local",
        "media_ult10_tarjetas_rojas_visitante",
        "tendencia_empate_h2h",
        "media_h2h_posesion_local",
        "media_h2h_posesion_visitante",
        "media_h2h_corners_local",
        "media_h2h_corners_visitante",
        "media_h2h_tarjetas_amarillas_local",
        "media_h2h_tarjetas_amarillas_visitante",
        "media_h2h_tarjetas_rojas_local",
        "media_h2h_tarjetas_rojas_visitante",
        "media_hist_posesion_local",
        "media_hist_posesion_visitante",
        "media_hist_corners_local",
        "media_hist_corners_visitante",
        "media_hist_tarjetas_amarillas_local",
        "media_hist_tarjetas_amarillas_visitante",
        "media_hist_tarjetas_rojas_local",
        "media_hist_tarjetas_rojas_visitante",
        "media_ult10_diferencia_goles_local",
        "media_ult10_diferencia_goles_visitante",
        "media_h2h_diferencia_goles_local",
        "media_h2h_diferencia_goles_visitante",
        "media_hist_diferencia_goles_local",
        "media_hist_diferencia_goles_visitante",
        "racha_ganados_local_ult5",
        "racha_ganados_visitante_ult5",
        "diferencia_posesion",
        "diferencia_corners",
        "diferencia_tarjetas_amarillas",
        "diferencia_tarjetas_rojas",
        "media_hist_goles_local_a_favor",
        "media_hist_goles_local_en_contra",
        "racha_empates_local_ult5",
        "racha_derrotas_local_ult5",
        "racha_empates_visitante_ult5",
        "racha_derrotas_visitante_ult5",
        "goles_local_ult5_media",
        "goles_visitante_ult5_media",
        "tendencia_empate_local",
        "tendencia_empate_visitante",
    ]

    def __init__(self, db_session: Session):
        self.partido_repo = PartidoRepository(db_session)
        self.team_repo = TeamRepository(db_session)

    def _format_shap_explanations(
        self,
        shap_values: np.ndarray,
        feature_names: List[str],
        feature_values: np.ndarray,
        top_n: int = 3
    ) -> List[str]:
        """Genera una explicación a partir de los valores SHAP"""

        if not (len(feature_names) == len(feature_values[0]) == len(shap_values)):
            error_msg = (
                f"Discrepancia de longitud detectada. "
                f"Nombres: {len(feature_names)}, "
                f"Valores: {len(feature_values[0])}, "
                f"SHAP: {len(shap_values)}"
            )
            return ["Error interno al procesar explicaciones: " + error_msg]

        try:
            explanations = []
            shap_df = pd.DataFrame({
                'feature': feature_names,
                'value': feature_values[0],
                'shap_value': shap_values
            })
            shap_df['abs_shap'] = shap_df['shap_value'].abs()
            top_features = shap_df.sort_values(by='abs_shap', ascending=False).head(top_n)

            for _, row in top_features.iterrows():
                raw_name = row['feature']
                feature_name = raw_name.replace("_", " ").title()
                value = row['value']
                shap_val = row['shap_value']

                if isinstance(value, float):
                    if "posesion" in raw_name:
                        value_str = f"{value:.1f}%"
                    elif "tendencia_empate" in raw_name:
                        value_str = f"{value * 100:.1f}%"
                    elif "diferencia_goles" in raw_name:
                        value_str = f"{value:.2f} goles"
                    elif "goles_" in raw_name:
                        value_str = f"{value:.2f} goles"
                    elif "corners" in raw_name:
                        value_str = f"{value:.2f} córners"
                    elif "tarjetas_amarillas" in raw_name:
                        value_str = f"{value:.2f} tarjetas amarillas"
                    elif "tarjetas_rojas" in raw_name:
                        value_str = f"{value:.2f} tarjetas rojas"
                    else:
                        value_str = f"{value:.2f}"
                else:
                    value_str = str(value)

                tag = "[INFLUENCIA POSITIVA]" if shap_val > 0.001 else "[INFLUENCIA NEGATIVA]"
                direction = "aumentó la probabilidad" if shap_val > 0.001 else "disminuyó la probabilidad"

                explanations.append(
                    f"{tag} La variable '{feature_name}' con valor '{value_str}' {direction} del resultado predicho."
                )

            return explanations

        except Exception:
            return ["No se pudieron generar las explicaciones detalladas para esta predicción."]

    def _get_match_result(self, partido: Any, team_id: str) -> int:
        """Calcula el resultado del partido de un equipo"""

        if partido.goles_local is None or partido.goles_visitante is None:
            return 0
        if partido.goles_local == partido.goles_visitante:
            return 0
        return 1 if (
            (partido.equipo_local_id == team_id and partido.goles_local > partido.goles_visitante) or
            (partido.equipo_visitante_id == team_id and partido.goles_visitante > partido.goles_local)
        ) else -1

    def _calculate_team_match_stats(self, partido: Any, stats: Any, team_id: str) -> Dict[str, Any]:
        """Obtiene las estadisticas de un equipo en un partido"""

        is_local = (partido.equipo_local_id == team_id)
        base_stats = {
            "goles_a_favor": partido.goles_local if is_local else partido.goles_visitante,
            "goles_en_contra": partido.goles_visitante if is_local else partido.goles_local,
            "es_local": is_local,
            "resultado": self._get_match_result(partido, team_id)
        }

        if not stats:
            base_stats.update({
                "posesion": np.nan,
                "corners": np.nan,
                "tarjetas_amarillas": np.nan,
                "tarjetas_rojas": np.nan
            })
            return base_stats

        raw_pos = stats.posesion_local if is_local else stats.posesion_visitante
        pos_norm = (raw_pos / 100.0) if raw_pos is not None else np.nan

        base_stats.update({
            "posesion": pos_norm,
            "corners": stats.corners_local if is_local else stats.corners_visitante,
            "tarjetas_amarillas": stats.tarjetas_amarillas_local if is_local else stats.tarjetas_amarillas_visitante,
            "tarjetas_rojas": stats.tarjetas_rojas_local if is_local else stats.tarjetas_rojas_visitante
        })
        return base_stats

    def _get_team_historical_data(self, team_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """ Recupera el historico de partidos de un equipo"""
        matches_with_stats = self.partido_repo.get_historical_matches_with_stats(team_id, match_date, limit=limit)
        return [self._calculate_team_match_stats(p, s, team_id) for p, s in matches_with_stats]

    def _get_h2h_historical_data(self, team1_id: str, team2_id: str, match_date: date, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """ Recupera el historico de los enfrentamientos H2H entre dos equipos"""
        matches_with_stats = self.partido_repo.get_h2h_matches_with_stats(team1_id, team2_id, match_date, limit=limit)
        h2h_data = []

        for partido, stats in matches_with_stats:
            team1_stats = self._calculate_team_match_stats(partido, stats, team1_id)
            team2_stats = self._calculate_team_match_stats(partido, stats, team2_id)

            data_point = {
                "local_goles": team1_stats.get("goles_a_favor"),
                "visitor_goles": team2_stats.get("goles_a_favor"),
                "resultado_local_perspective": team1_stats.get("resultado"),
                "local_posesion": team1_stats.get("posesion"),
                "visitor_posesion": team2_stats.get("posesion"),
                "local_corners": team1_stats.get("corners"),
                "visitor_corners": team2_stats.get("corners"),
                "local_tarjetas_amarillas": team1_stats.get("tarjetas_amarillas"),
                "visitor_tarjetas_amarillas": team2_stats.get("tarjetas_amarillas"),
                "local_tarjetas_rojas": team1_stats.get("tarjetas_rojas"),
                "visitor_tarjetas_rojas": team2_stats.get("tarjetas_rojas")
            }

            h2h_data.append(data_point)

        return h2h_data

    def _calculate_average_stats(self, data: List[Dict[str, Any]], stat_key: str) -> float:
        """Calcula la media de una estadística concreta"""

        values = [d.get(stat_key) for d in data]
        values = [v for v in values if v is not None and not np.isnan(v)]
        return float(np.mean(values)) if values else np.nan
    
    def _avg_from_team_perspective(self, matches_with_stats, team_id: str, stat_key: str) -> float:
        """Calcula la media de una estadística de un equipo"""

        vals = []
        for partido, stats in matches_with_stats:
            team_stats = self._calculate_team_match_stats(partido, stats, team_id)
            v = team_stats.get(stat_key, np.nan)
            if v is None or np.isnan(v):
                continue
            vals.append(float(v))
        return float(np.mean(vals)) if vals else np.nan
    
    def _calculate_features_for_single_match(self, local_team_id: str, visitor_team_id: str, match_date: date) -> pd.DataFrame:
        """Calcula las variables necesarias para hacer la predicción"""

        features: Dict[str, Any] = {}

        local_ult10 = self._get_team_historical_data(local_team_id, match_date, 10)
        visitor_ult10 = self._get_team_historical_data(visitor_team_id, match_date, 10)

        if not local_ult10 or not visitor_ult10:
            raise ValueError("Datos históricos insuficientes de los ultimos 10 partidos para generar la predicción.")

        local_ult10_raw = self.partido_repo.get_historical_matches_with_stats(local_team_id, match_date, limit=10)
        visitor_ult10_raw = self.partido_repo.get_historical_matches_with_stats(visitor_team_id, match_date, limit=10)

        local_hist_raw = self.partido_repo.get_historical_matches_with_stats(local_team_id, match_date, limit=None)
        visitor_hist_raw = self.partido_repo.get_historical_matches_with_stats(visitor_team_id, match_date, limit=None)

        h2h = self._get_h2h_historical_data(local_team_id, visitor_team_id, match_date, 10)
        local_hist = self._get_team_historical_data(local_team_id, match_date)
        visitor_hist = self._get_team_historical_data(visitor_team_id, match_date)

        local_ult5 = local_ult10[:5]
        visitor_ult5 = visitor_ult10[:5]

        posesion_local = self._calculate_average_stats(local_ult10, "posesion")
        posesion_visitante = self._calculate_average_stats(visitor_ult10, "posesion")

        features["posesion_local"] = posesion_local * 100 if not np.isnan(posesion_local) else np.nan
        features["posesion_visitante"] = posesion_visitante * 100 if not np.isnan(posesion_visitante) else np.nan
        features["corners_local"] = self._calculate_average_stats(local_ult10, "corners")
        features["corners_visitante"] = self._calculate_average_stats(visitor_ult10, "corners")
        features["tarjetas_amarillas_local"] = self._calculate_average_stats(local_ult10, "tarjetas_amarillas")
        features["tarjetas_amarillas_visitante"] = self._calculate_average_stats(visitor_ult10, "tarjetas_amarillas")
        features["tarjetas_rojas_local"] = self._calculate_average_stats(local_ult10, "tarjetas_rojas")
        features["tarjetas_rojas_visitante"] = self._calculate_average_stats(visitor_ult10, "tarjetas_rojas")

        for stat in ["posesion", "corners", "tarjetas_amarillas", "tarjetas_rojas"]:
            features[f"media_ult10_{stat}_local"] = self._avg_from_team_perspective(local_ult10_raw, local_team_id, stat)
            features[f"media_ult10_{stat}_visitante"] = self._avg_from_team_perspective(visitor_ult10_raw, visitor_team_id, stat)

            features[f"media_hist_{stat}_local"] = self._avg_from_team_perspective(local_hist_raw, local_team_id, stat)
            features[f"media_hist_{stat}_visitante"] = self._avg_from_team_perspective(visitor_hist_raw, visitor_team_id, stat)

            l_vals = [d.get(f"local_{stat}") for d in h2h if d.get(f"local_{stat}") is not None and not np.isnan(d.get(f"local_{stat}"))]
            v_vals = [d.get(f"visitor_{stat}") for d in h2h if d.get(f"visitor_{stat}") is not None and not np.isnan(d.get(f"visitor_{stat}"))]

            features[f"media_h2h_{stat}_local"] = float(np.mean(l_vals)) if l_vals else np.nan
            features[f"media_h2h_{stat}_visitante"] = float(np.mean(v_vals)) if v_vals else np.nan
        if h2h:
            features["tendencia_empate_h2h"] = float(np.mean([1 if d.get("resultado_local_perspective") == 0 else 0 for d in h2h]))
        else:
            features["tendencia_empate_h2h"] = 0.0

        features["media_ult10_diferencia_goles_local"] = self._calculate_average_stats(local_ult10, "goles_a_favor") - self._calculate_average_stats(local_ult10, "goles_en_contra")
        features["media_ult10_diferencia_goles_visitante"] = self._calculate_average_stats(visitor_ult10, "goles_a_favor") - self._calculate_average_stats(visitor_ult10, "goles_en_contra")

        h2h_matches = self.partido_repo.get_h2h_matches_with_stats(local_team_id, visitor_team_id, match_date, limit=10)
        h2h_diffs_local = []
        h2h_diffs_visitante = []

        for partido, _stats in h2h_matches:
            if partido.goles_local is None or partido.goles_visitante is None:
                continue

            if partido.equipo_local_id == local_team_id:
                gf_l, ga_l = partido.goles_local, partido.goles_visitante
            else:
                gf_l, ga_l = partido.goles_visitante, partido.goles_local
            h2h_diffs_local.append(gf_l - ga_l)

            if partido.equipo_local_id == visitor_team_id:
                gf_v, ga_v = partido.goles_local, partido.goles_visitante
            else:
                gf_v, ga_v = partido.goles_visitante, partido.goles_local
            h2h_diffs_visitante.append(gf_v - ga_v)

        features["media_h2h_diferencia_goles_local"] = float(np.mean(h2h_diffs_local)) if h2h_diffs_local else np.nan
        features["media_h2h_diferencia_goles_visitante"] = float(np.mean(h2h_diffs_visitante)) if h2h_diffs_visitante else np.nan

        features["media_hist_diferencia_goles_local"] = self._calculate_average_stats(local_hist, "goles_a_favor") - self._calculate_average_stats(local_hist, "goles_en_contra")
        features["media_hist_diferencia_goles_visitante"] = self._calculate_average_stats(visitor_hist, "goles_a_favor") - self._calculate_average_stats(visitor_hist, "goles_en_contra")

        for r_type, r_name in zip([1, 0, -1], ["ganados", "empates", "derrotas"]):
            features[f"racha_{r_name}_local_ult5"] = sum(1 for d in local_ult5 if d.get("resultado") == r_type)
            features[f"racha_{r_name}_visitante_ult5"] = sum(1 for d in visitor_ult5 if d.get("resultado") == r_type)

        features["diferencia_posesion"] = features.get("media_ult10_posesion_local", np.nan) - features.get("media_ult10_posesion_visitante", np.nan)
        features["diferencia_corners"] = features.get("media_ult10_corners_local", np.nan) - features.get("media_ult10_corners_visitante", np.nan)
        features["diferencia_tarjetas_amarillas"] = features.get("media_ult10_tarjetas_amarillas_local", np.nan) - features.get("media_ult10_tarjetas_amarillas_visitante", np.nan)
        features["diferencia_tarjetas_rojas"] = features.get("media_ult10_tarjetas_rojas_local", np.nan) - features.get("media_ult10_tarjetas_rojas_visitante", np.nan)

        local_home_matches = [d for d in local_hist if d.get("es_local")]
        features["media_hist_goles_local_a_favor"] = self._calculate_average_stats(local_home_matches, "goles_a_favor")
        features["media_hist_goles_local_en_contra"] = self._calculate_average_stats(local_home_matches, "goles_en_contra")

        features["goles_local_ult5_media"] = self._calculate_average_stats(local_ult5, "goles_a_favor")
        features["goles_visitante_ult5_media"] = self._calculate_average_stats(visitor_ult5, "goles_a_favor")

        if local_ult10:
            features["tendencia_empate_local"] = float(np.mean([1 if d.get("resultado") == 0 else 0 for d in local_ult10]))
        else:
            features["tendencia_empate_local"] = 0.0

        if visitor_ult10:
            features["tendencia_empate_visitante"] = float(np.mean([1 if d.get("resultado") == 0 else 0 for d in visitor_ult10]))
        else:
            features["tendencia_empate_visitante"] = 0.0

        features_df = pd.DataFrame([features])

        percent_cols = [
            "media_ult10_posesion_local",
            "media_ult10_posesion_visitante",
            "media_h2h_posesion_local",
            "media_h2h_posesion_visitante",
            "media_hist_posesion_local",
            "media_hist_posesion_visitante",
        ]
        for col in percent_cols:
            if col in features_df.columns:
                features_df[col] = features_df[col] * 100.0

        if {"media_ult10_posesion_local", "media_ult10_posesion_visitante"}.issubset(features_df.columns):
            features_df["diferencia_posesion"] = features_df["media_ult10_posesion_local"] - features_df["media_ult10_posesion_visitante"]

        return features_df

    def predict_match_result(
            self,
            local_team_name: str,
            visitor_team_name: str,
            match_date: date,
            ml_model: MLPClassifier,
            explainer: shap.KernelExplainer
        ) -> Tuple[str, Dict[str, float], List[str]]:
        """Genera la predicción del partido a partir de los equipos y la fecha"""

        local_team = self.team_repo.get_team_by_name(local_team_name)
        if not local_team:
            raise ValueError(f"Equipo local '{local_team_name}' no encontrado.")

        visitor_team = self.team_repo.get_team_by_name(visitor_team_name)
        if not visitor_team:
            raise ValueError(f"Equipo visitante '{visitor_team_name}' no encontrado.")

        features_df_raw = self._calculate_features_for_single_match(local_team.equipo_id, visitor_team.equipo_id, match_date)
        final_features_df = features_df_raw.reindex(columns=self._MODEL_FEATURES).fillna(0)

        predicted_class_int = ml_model.predict(final_features_df)[0]
        probabilities = ml_model.predict_proba(final_features_df)[0]

        explanations: List[str] = []
        try:
            explanation_object = explainer(final_features_df)
            class_index_map = {val: i for i, val in enumerate(ml_model.classes_)}
            predicted_class_index = class_index_map.get(int(predicted_class_int), 0)
            shap_values_for_predicted_class = explanation_object.values[0, :, predicted_class_index]

            explanations = self._format_shap_explanations(
                shap_values_for_predicted_class,
                list(final_features_df.columns),
                final_features_df.values
            )
        except Exception:
            explanations = ["Las explicaciones detalladas no están disponibles en este momento."]

        result_map = {1: "Victoria Local", 0: "Empate", -1: "Victoria Visitante"}
        predicted_result_str = result_map.get(int(predicted_class_int), "Desconocido")

        prob_dict = {result_map[int(label)]: prob for label, prob in zip(ml_model.classes_, probabilities)}
        final_probs = {
            "Victoria Local": float(prob_dict.get("Victoria Local", 0.0)),
            "Empate": float(prob_dict.get("Empate", 0.0)),
            "Victoria Visitante": float(prob_dict.get("Victoria Visitante", 0.0))
        }

        return predicted_result_str, final_probs, explanations
