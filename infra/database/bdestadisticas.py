import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import and_
from sqlalchemy.orm import aliased
from infra.database.mysql_connect import get_session
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido
from domain.models.estadisticas_partido_csv import EstadisticasPartidoCSV

def main():
    session = get_session()

    e1 = aliased(EstadisticasPartidoCSV)
    e2 = aliased(EstadisticasPartidoCSV)

    query = (
        session.query(
            Partido.partido_id,
            e1.posesion.label("posesion_local"),
            e2.posesion.label("posesion_visitante"),
            e1.corners.label("corners_local"),
            e2.corners.label("corners_visitante"),
            e1.amarillas.label("tarjetas_amarillas_local"),
            e2.amarillas.label("tarjetas_amarillas_visitante"),
            e1.rojas.label("tarjetas_rojas_local"),
            e2.rojas.label("tarjetas_rojas_visitante"),
        )
        .outerjoin(e1, and_(Partido.partido_id == e1.partido_id, Partido.equipo_local_id == e1.equipo_id))
        .outerjoin(e2, and_(Partido.partido_id == e2.partido_id, Partido.equipo_visitante_id == e2.equipo_id))
    )

    for row in query.all():
        estadistica = EstadisticasPartido(
            partido_id=row.partido_id,
            posesion_local=row.posesion_local,
            posesion_visitante=row.posesion_visitante,
            corners_local=row.corners_local,
            corners_visitante=row.corners_visitante,
            tarjetas_amarillas_local=row.tarjetas_amarillas_local,
            tarjetas_amarillas_visitante=row.tarjetas_amarillas_visitante,
            tarjetas_rojas_local=row.tarjetas_rojas_local,
            tarjetas_rojas_visitante=row.tarjetas_rojas_visitante,
        )
        session.add(estadistica)  #  Esto debe estar dentro del bucle

    session.commit()
    session.close()
    print(" Datos insertados correctamente en estadisticas_partido.")

if __name__ == "__main__":
    main()
