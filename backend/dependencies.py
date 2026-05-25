import os
from typing import Iterator, Optional, Tuple

import joblib
import shap
from sqlalchemy.orm import Session
from sklearn.neural_network import MLPClassifier

from infra.database.mysql_connect import get_session

ML_MODEL_PATH = os.getenv("ML_MODEL_PATH")
EXPLAINER_PATH = os.getenv("EXPLAINER_PATH")

ml_model: Optional[MLPClassifier] = None
explainer: Optional[shap.KernelExplainer] = None

def load_prediction_artifacts():
    """Carga en memoria el modelo y el explainer al iniciar la aplicación."""
    
    global ml_model, explainer
    if ml_model is None or explainer is None:
        try:
            if not ML_MODEL_PATH or not EXPLAINER_PATH:
                raise ValueError("Una o más variables de entorno de los modelos no están definidas.")
            
            ml_model = joblib.load(ML_MODEL_PATH)
            explainer = joblib.load(EXPLAINER_PATH)

        except Exception as e:
            raise RuntimeError(f"No se pudieron cargar los recursos del modelo: {e}")

def get_db_session() -> Iterator[Session]:
    """Proporciona una session de base de datos para las dependencias de FastAPI."""

    session = get_session()
    try:
        yield session
    finally:
        session.close()

def get_prediction_pipeline() -> Tuple[MLPClassifier, shap.KernelExplainer]:
    """Devuelve el modelo y el explainer para realizar las predicciones"""

    if ml_model is None or explainer is None:
        raise RuntimeError("Los recursos del modelo no estan disponibles.")
    return ml_model, explainer