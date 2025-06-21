from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import date

# --- Schemas para Equipo (lectura) ---
class TeamResponse(BaseModel):
    equipo_id: str = Field(..., description="ID único del equipo (ej. 'ARS', 'RMA')")
    nombre: str = Field(..., description="Nombre completo del equipo (ej. 'Arsenal')")
    abreviatura: str = Field(..., description="Abreviatura del equipo (ej. 'ARS')")

    class Config:
        from_attributes = True  # Usado en Pydantic v2 en lugar de orm_mode = True


# --- Schemas para Predicción ---
class PredictionRequest(BaseModel):
    local_team_name: str = Field(..., alias="equipo_local", description="Nombre del equipo local")
    visitor_team_name: str = Field(..., alias="equipo_visitante", description="Nombre del equipo visitante")
    match_date: Optional[date] = Field(None, description="Fecha del partido (opcional, para contexto histórico de features)")

    class Config:
        populate_by_name = True  # Permite usar los aliases al crear instancias con nombre de campos originales


class PredictionResponse(BaseModel):
    predicted_result: str = Field(..., description="Resultado predicho: 'Victoria Local', 'Empate' o 'Victoria Visitante'")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades de cada resultado (Victoria Local, Empate, Victoria Visitante)")

    # Descomenta si implementas explicaciones SHAP
    # shap_values: Optional[Dict[str, float]] = None
    # base_value: Optional[float] = None
