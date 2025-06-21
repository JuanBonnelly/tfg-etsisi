# backend/repositories/partido_repository.py
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Tuple
from datetime import date

# Importa tus modelos ORM
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido # Asegura la importación

class PartidoRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_historical_matches_with_stats(self, team_id: str, before_date: date, limit: Optional[int] = None) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene partidos históricos para un equipo con sus estadísticas, antes de una fecha específica.
        Retorna una lista de tuplas (Partido, EstadisticasPartido).
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                or_(Partido.equipo_local_id == team_id, Partido.equipo_visitante_id == team_id),
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_h2h_matches_with_stats(self, team1_id: str, team2_id: str, before_date: date, limit: Optional[int] = None) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene enfrentamientos directos (H2H) entre dos equipos con sus estadísticas, antes de una fecha específica.
        Retorna una lista de tuplas (Partido, EstadisticasPartido).
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                or_(
                    and_(Partido.equipo_local_id == team1_id, Partido.equipo_visitante_id == team2_id),
                    and_(Partido.equipo_local_id == team2_id, Partido.equipo_visitante_id == team1_id)
                ),
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())

        if limit:
            query = query.limit(limit)

        return query.all()

    def get_team_home_matches_with_stats(self, team_id: str, before_date: date) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """
        Obtiene partidos históricos donde un equipo fue local, con sus estadísticas.
        """
        query = self.db_session.query(Partido, EstadisticasPartido).\
            outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id).\
            filter(
                Partido.equipo_local_id == team_id,
                Partido.fecha < before_date
            ).\
            order_by(Partido.fecha.desc())
        return query.all()

    # Puedes añadir un método para obtener las estadísticas del partido actual si las necesitaras en las features
    # def get_match_stats_by_id(self, partido_id: str) -> Optional[EstadisticasPartido]:
    #     return self.db_session.query(EstadisticasPartido).filter(EstadisticasPartido.partido_id == partido_id).first()