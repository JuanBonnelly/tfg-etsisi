# backend/schemas.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date

# --- Schemas para Equipo ---
class TeamResponse(BaseModel):
    team_id: str = Field(..., description="ID único del equipo (ej. 'ARS', 'RMA')")
    name: str = Field(..., description="Nombre completo del equipo (ej. 'Arsenal')")
    abreviatura: str = Field(..., description="Abreviatura del equipo (ej. 'ARS')")

    class Config:
        from_attributes = True # Permite crear el modelo desde un objeto ORM

# --- Schemas para Predicción (se completarán en Tarea 2.1) ---
class PredictionRequest(BaseModel):
    local_team_name: str = Field(..., description="Nombre del equipo local")
    visitor_team_name: str = Field(..., description="Nombre del equipo visitante")
    match_date: Optional[date] = Field(None, description="Fecha del partido (opcional, para contexto histórico de features)")

class PredictionResponse(BaseModel):
    predicted_result: str = Field(..., description="Resultado predicho: 'Victoria Local', 'Empate' o 'Victoria Visitante'")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades de cada resultado (Victoria Local, Empate, Victoria Visitante)")
    # shap_values: Optional[Dict[str, float]] = None # Opcional: si implementas explicaciones SHAP
    # base_value: Optional[float] = None # Opcional: si implementas explicaciones SHAP