from datetime import date
from typing import Dict, Optional, List

from pydantic import BaseModel, Field



class TeamResponse(BaseModel):
    equipo_id: str = Field(..., description="ID único del equipo")
    nombre: str = Field(..., description="Nombre completo del equipo")
    abreviatura: str = Field(..., description="Abreviatura del equipo")

    class Config:
        from_attributes = True

class PredictionRequest(BaseModel):
    local_team_name: str = Field(..., alias="equipo_local", description="Nombre del equipo local")
    visitor_team_name: str = Field(..., alias="equipo_visitante", description="Nombre del equipo visitante")
    match_date: Optional[date] = Field(None, description="Fecha del partido")
    
    class Config:
        populate_by_name = True

class PredictionResponse(BaseModel):
    predicted_result: str = Field(..., description="Resultado predicho:'V','E'o'D'")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades de cada resultado ('V','E','D')")
    explanations: List[str] = Field(..., description="Lista de las principales razones que influyeron en la predicción.")