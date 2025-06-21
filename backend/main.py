# backend/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Tuple
from datetime import date
from contextlib import asynccontextmanager
import traceback

from backend.dependencies import get_db_session, load_ml_artifacts, get_prediction_pipeline
from backend.services.team_service import TeamService
from backend.services.prediction_service import PredictionService
from backend.schemas import TeamResponse, PredictionRequest, PredictionResponse

from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- DEBUG [main]: Iniciando lifespan...")
    load_ml_artifacts()
    print("--- DEBUG [main]: Lifespan iniciado, recursos cargados.")
    yield
    print("--- DEBUG [main]: Finalizando lifespan...")

app = FastAPI(
    title="API de Predicción de Partidos de Fútbol",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/")
async def root():
    print("--- DEBUG: ¡La petición a la ruta raíz '/' ha sido recibida! ---")
    return {"message": "API de Predicción de Fútbol iniciada y respondiendo."}

@app.get("/teams", response_model=List[TeamResponse])
async def get_teams(db_session: Session = Depends(get_db_session)):
    print("--- DEBUG [main]: Recibida petición para /teams")
    team_service = TeamService(db_session)
    return team_service.get_teams_list()

@app.post("/predict", response_model=PredictionResponse)
async def predict_match(
    request: PredictionRequest,
    db_session: Session = Depends(get_db_session),
    ml_pipeline: Tuple[RandomForestClassifier, StandardScaler] = Depends(get_prediction_pipeline)
):
    print("\n--- DEBUG [main]: ================== INICIO PETICIÓN /predict ================== ---")
    print(f"--- DEBUG [main]: Request recibido: {request.model_dump_json()}")
    
    ml_model, scaler = ml_pipeline
    
    try:
        print("--- DEBUG [main]: Creando PredictionService...")
        prediction_service = PredictionService(db_session)
        
        print("--- DEBUG [main]: Llamando a prediction_service.predict_match_result...")
        predicted_result_str, probabilities = prediction_service.predict_match_result(
            local_team_name=request.local_team_name,
            visitor_team_name=request.visitor_team_name,
            match_date=request.match_date or date.today(),
            ml_model=ml_model,
            scaler=scaler
        )
        
        print(f"--- DEBUG [main]: Servicio devolvió: Resultado='{predicted_result_str}', Probs={probabilities}")
        response_data = PredictionResponse(
            predicted_result=predicted_result_str,
            probabilities=probabilities
        )
        
        print("--- DEBUG [main]: Enviando respuesta 200 OK.")
        print("--- DEBUG [main]: ================== FIN PETICIÓN /predict ================== ---\n")
        return response_data
        
    except ValueError as e:
        print(f"--- DEBUG [main]: Capturado ValueError (se devolverá 400): {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        print(f"--- DEBUG [main]: ¡¡¡Capturada Excepción Inesperada (se devolverá 500)!!!")
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Ocurrió un error interno en el servidor.")