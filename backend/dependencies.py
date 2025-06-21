# backend/dependencies.py
import joblib
import os
import traceback
from sqlalchemy.orm import Session
from typing import Optional, Tuple, Iterator

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from infra.database.mysql_connect import get_session

# Rutas a los modelos ML
ML_MODEL_PATH = os.getenv("ML_MODEL_PATH")
SCALER_PATH = os.getenv("SCALER_PATH")

# Variables globales para almacenar los artefactos
ml_model: Optional[RandomForestClassifier] = None
scaler: Optional[StandardScaler] = None

def load_ml_artifacts():
    global ml_model, scaler
    print("--- DEBUG [deps]: Intentando cargar artefactos ML...")
    if ml_model is None or scaler is None:
        try:
            if not ML_MODEL_PATH or not SCALER_PATH:
                raise ValueError("Variables de entorno ML_MODEL_PATH o SCALER_PATH no definidas.")
            
            print(f"--- DEBUG [deps]: Cargando modelo ML desde: {ML_MODEL_PATH}")
            ml_model = joblib.load(ML_MODEL_PATH)
            
            print(f"--- DEBUG [deps]: Cargando scaler desde: {SCALER_PATH}")
            scaler = joblib.load(SCALER_PATH)
            
            print("--- DEBUG [deps]: Modelo y Scaler cargados exitosamente.")
            
        except Exception as e:
            print(f"--- DEBUG [deps]: ¡¡¡ERROR CRÍTICO AL CARGAR ARTEFACTOS ML!!! ---")
            traceback.print_exc()
            raise RuntimeError(f"Error al cargar recursos ML: {e}")
    else:
        print("--- DEBUG [deps]: Modelo y Scaler ya estaban cargados.")

def get_db_session() -> Iterator[Session]:
    print("--- DEBUG [deps]: Creando sesión de BD...")
    session = get_session()
    try:
        yield session
    finally:
        print("--- DEBUG [deps]: Cerrando sesión de BD.")
        session.close()

def get_prediction_pipeline() -> Tuple[RandomForestClassifier, StandardScaler]:
    print("--- DEBUG [deps]: Proporcionando pipeline de predicción (modelo y scaler)...")
    if ml_model is None or scaler is None:
        raise RuntimeError("Modelo ML o Scaler no disponibles. Verificar logs de startup.")
    return ml_model, scaler