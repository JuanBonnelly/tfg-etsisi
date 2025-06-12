# backend/repositories/team_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional

# Importa tu modelo ORM Equipo
from domain.models.equipo import Equipo

class TeamRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_all_teams(self) -> List[Equipo]:
        """Obtiene todos los equipos de la base de datos, ordenados por nombre."""
        return self.db_session.query(Equipo).order_by(Equipo.nombre).all()

    def get_team_by_name(self, name: str) -> Optional[Equipo]:
        """Obtiene un equipo por su nombre."""
        return self.db_session.query(Equipo).filter(Equipo.nombre == name).first()

    def get_team_by_id(self, team_id: str) -> Optional[Equipo]:
        """Obtiene un equipo por su ID."""
        return self.db_session.query(Equipo).filter(Equipo.equipo_id == team_id).first()