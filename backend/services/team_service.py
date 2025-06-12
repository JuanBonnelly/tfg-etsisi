# backend/services/team_service.py
from typing import List, Optional
from sqlalchemy.orm import Session

# Importa el repositorio y el esquema de respuesta
from backend.repositories.team_repository import TeamRepository
from backend.schemas import TeamResponse

class TeamService:
    def __init__(self, db_session: Session):
        self.team_repo = TeamRepository(db_session)

    def get_teams_list(self) -> List[TeamResponse]:
        """
        Obtiene la lista de todos los equipos y los formatea como TeamResponse.
        """
        teams = self.team_repo.get_all_teams()
        return [TeamResponse.model_validate(team) for team in teams]

    def get_team_id_by_name(self, team_name: str) -> Optional[str]:
        """
        Busca un equipo por su nombre y retorna su ID si existe.
        """
        team = self.team_repo.get_team_by_name(team_name)
        return team.equipo_id if team else None