from contextlib import asynccontextmanager
from datetime import date
from typing import List, Tuple

import shap
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sklearn.neural_network import MLPClassifier

from backend.dependencies import get_db_session, get_prediction_pipeline, load_prediction_artifacts
from backend.schemas import PredictionRequest, PredictionResponse, TeamResponse
from backend.services.prediction_service import PredictionService
from backend.services.team_service import TeamService

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_prediction_artifacts()
    yield


app = FastAPI(
    title="API de Predicción de Partidos de Fútbol",
    version="1.0.0",
    description="API que utiliza un modelo MLP y explicaciones SHAP para predecir resultados de fútbol.",
    lifespan=lifespan,
)

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Comprobación de estado")
async def get_status():
    """Comprueba que la API está disponible."""
    
    return {"message": "API de predicción de fútbol disponible."}


@app.get("/teams", response_model=List[TeamResponse], summary="Obtener lista de equipos")
async def get_teams(db_session: Session = Depends(get_db_session)):
    """Devuelve la lista de equipos disponibles."""

    team_service = TeamService(db_session)
    return team_service.get_teams_list()


@app.post("/predict", response_model=PredictionResponse, summary="Realizar una predicción")
async def predict_match(
    request: PredictionRequest,
    db_session: Session = Depends(get_db_session),
    ml_pipeline: Tuple[MLPClassifier, shap.KernelExplainer] = Depends(get_prediction_pipeline),
):
    """Genera la predicción de un partido a partir de los equipos y la fecha indicada."""

    ml_model, explainer = ml_pipeline
    prediction_service = PredictionService(db_session)

    try:
        predicted_result_str, probabilities, explanations = prediction_service.predict_match_result(
            local_team_name=request.local_team_name,
            visitor_team_name=request.visitor_team_name,
            match_date=request.match_date or date.today(),
            ml_model=ml_model,
            explainer=explainer,
        )

        return PredictionResponse(
            predicted_result=predicted_result_str,
            probabilities=probabilities,
            explanations=explanations,
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno al procesar la predicción.",
        )