# backend/dependencies.py
import joblib
import os
from sklearn.neural_network import MLPClassifier # Importa el tipo de tu modelo
from sklearn.preprocessing import StandardScaler # Importa el tipo de tu scaler
from sqlalchemy.orm import Session
from typing import Optional, Tuple

# Importa tu función de conexión a la base de datos
from infra.database.mysql_connect import get_session

# Rutas a los modelos ML (se obtienen de las variables de entorno de Docker Compose)
ML_MODEL_PATH = os.getenv("ML_MODEL_PATH")
SCALER_PATH = os.getenv("SCALER_PATH")

# Variables globales para almacenar el modelo y el scaler cargados
ml_model: Optional[MLPClassifier] = None
scaler: Optional[StandardScaler] = None

def load_ml_artifacts():
    """
    Carga el modelo de ML y el scaler una única vez al inicio de la aplicación.
    """
    global ml_model, scaler
    if ml_model is None or scaler is None:
        try:
            print(f"Cargando modelo ML desde: {ML_MODEL_PATH}")
            ml_model = joblib.load(ML_MODEL_PATH)
            print(f"Cargando scaler desde: {SCALER_PATH}")
            scaler = joblib.load(SCALER_PATH)
            print("Modelo ML y Scaler cargados exitosamente.")
        except FileNotFoundError as e:
            print(f"ERROR: Archivo de modelo o scaler no encontrado. Verifica las rutas en docker-compose.yml y Dockerfile.backend. Error: {e}")
            raise RuntimeError(f"Error al cargar recursos ML: {e}. Asegúrate de que los archivos existan en el path esperado dentro del contenedor.")
        except Exception as e:
            print(f"ERROR: Error inesperado al cargar recursos ML: {e}")
            raise RuntimeError(f"Error inesperado al cargar recursos ML: {e}")
    return ml_model, scaler

def get_db_session() -> Session:
    """
    Dependencia de FastAPI para obtener una sesión de base de datos.
    Asegura que la sesión se cierra automáticamente después de la solicitud.
    """
    session = get_session()
    try:
        yield session
    finally:
        session.close()

def get_prediction_pipeline() -> Tuple[MLPClassifier, StandardScaler]:
    """
    Dependencia de FastAPI que proporciona el modelo ML y el scaler cargados.
    Debe ser llamada después de que `load_ml_artifacts` haya inicializado las variables globales.
    """
    if ml_model is None or scaler is None:
        raise RuntimeError("Modelo ML o Scaler no disponibles. Verificar logs de startup.")
    return ml_model, scaler