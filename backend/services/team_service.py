from typing import List, Optional
from sqlalchemy.orm import Session
from backend.repositories.team_repository import TeamRepository
from backend.schemas import TeamResponse



class TeamService:
    def __init__(self, db_session: Session):
        self.team_repo = TeamRepository(db_session)

    def get_teams_list(self) -> List[TeamResponse]:
        """Devuelve la lista de equipos disponibles"""

        teams = self.team_repo.get_all_teams()
        return [TeamResponse.model_validate(team) for team in teams]

    def get_team_id_by_name(self, team_name: str) -> Optional[str]:
        """Devuelve el id de un equipo a partir de su nombre"""

        team = self.team_repo.get_team_by_name(team_name)
        return team.equipo_id if team else None