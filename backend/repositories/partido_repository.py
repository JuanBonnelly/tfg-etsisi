from datetime import date
from typing import List, Optional, Tuple

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido


class PartidoRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_historical_matches_with_stats(
        self,
        team_id: str,
        before_date: date,
        limit: Optional[int] = None
    ) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """Devuelve el histórico de un equipo junto a sus estadísticas"""

        query = (
            self.db_session.query(Partido, EstadisticasPartido)
            .outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id)
            .filter(
                or_(Partido.equipo_local_id == team_id, Partido.equipo_visitante_id == team_id),
                Partido.fecha < before_date
            )
            .order_by(Partido.fecha.desc())
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_h2h_matches_with_stats(
        self,
        team1_id: str,
        team2_id: str,
        before_date: date,
        limit: Optional[int] = None
    ) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """Devuelve el histórico de enfrentamientos entre los dos equipos junto sus estadísticas"""

        query = (
            self.db_session.query(Partido, EstadisticasPartido)
            .outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id)
            .filter(
                or_(
                    and_(Partido.equipo_local_id == team1_id, Partido.equipo_visitante_id == team2_id),
                    and_(Partido.equipo_local_id == team2_id, Partido.equipo_visitante_id == team1_id)
                ),
                Partido.fecha < before_date
            )
            .order_by(Partido.fecha.desc())
        )

        if limit is not None:
            query = query.limit(limit)

        return query.all()

    def get_team_home_matches_with_stats(
        self,
        team_id: str,
        before_date: date
    ) -> List[Tuple[Partido, Optional[EstadisticasPartido]]]:
        """Devuelve los equipos en casa de un equipo junto a sus estadísticas"""

        query = (
            self.db_session.query(Partido, EstadisticasPartido)
            .outerjoin(EstadisticasPartido, Partido.partido_id == EstadisticasPartido.partido_id)
            .filter(
                Partido.equipo_local_id == team_id,
                Partido.fecha < before_date
            )
            .order_by(Partido.fecha.desc())
        )

        return query.all()
