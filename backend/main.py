# backend/main.py (VERSION FINAL DE FASE 1 - para Tarea 1.6)
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Dict, Optional, Tuple
from datetime import date

# Importaciones de tus módulos del backend
from backend.dependencies import get_db_session, load_ml_artifacts, get_prediction_pipeline
from backend.services.team_service import TeamService
# from backend.services.prediction_service import PredictionService # Se importará en Fase 2
from backend.schemas import TeamResponse, PredictionRequest, PredictionResponse # PredictionRequest/Response se completarán en Fase 2

# Importaciones de los tipos de modelos ML para type hinting (del scikit-learn)
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

# --- Configuración de la aplicación FastAPI ---
app = FastAPI(
    title="API de Predicción de Partidos de Fútbol",
    description="API para predecir resultados de partidos de fútbol usando Machine Learning.",
    version="1.0.0"
)

# Configurar CORS (ajusta origins según tu frontend)
origins = [
    "http://localhost",
    "http://localhost:4200", # Puerto por defecto de Angular CLI en desarrollo
    "http://127.0.0.0:4200", # También útil para algunas configuraciones
    # Añade aquí la URL de tu frontend en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Endpoints ---

@app.get("/")
async def root():
    """
    Endpoint raíz para verificar que la API está funcionando.
    """
    return {"message": "API de Predicción de Fútbol iniciada. Visita /docs para la documentación."}

@app.get("/teams", response_model=List[TeamResponse])
async def get_teams(db_session: Session = Depends(get_db_session)):
    """
    Obtiene una lista de todos los equipos disponibles en la base de datos.
    """
    team_service = TeamService(db_session)
    teams = team_service.get_teams_list()
    return teams

# Placeholder para el endpoint de predicción (se implementará en la Fase 2)
@app.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_501_NOT_IMPLEMENTED)
async def predict_match(
    request: PredictionRequest,
    db_session: Session = Depends(get_db_session),
    ml_pipeline: Tuple[MLPClassifier, StandardScaler] = Depends(get_prediction_pipeline)
):
    """
    Predice el resultado de un partido entre dos equipos dados.
    NOTA: Este endpoint aún no está implementado.
    """
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Endpoint de predicción no implementado aún.")

# --- Eventos de la aplicación ---
@app.on_event("startup")
async def startup_event():
    """
    Evento que se ejecuta cuando la aplicación FastAPI arranca.
    Aquí cargamos los modelos de Machine Learning y el scaler una única vez.
    """
    print("Aplicación FastAPI iniciada. Cargando recursos...")
    load_ml_artifacts()
    print("Modelo ML y Scaler cargados (si las rutas son correctas y los archivos existen).")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Evento que se ejecuta cuando la aplicación FastAPI se cierra.
    """
    print("Aplicación FastAPI cerrada.")