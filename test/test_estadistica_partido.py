import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.partido import Partido
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada
from domain.models.competicion import Competicion
from domain.models.estadisticas_partido import EstadisticasPartido

# Crear las tablas
Base.metadata.create_all(get_engine())

session = get_session()

# ---------- Crear datos previos necesarios ----------
equipo1 = Equipo(nombre="Betis", abreviatura="BET")
equipo2 = Equipo(nombre="Cádiz", abreviatura="CAD")
competicion = Competicion(nombre="LaLiga", abreviatura="LL")
temporada = Temporada(año_inicio=2023, año_fin=2024, competicion_id=1)

session.add_all([equipo1, equipo2, competicion, temporada])
session.commit()

# ---------- Crear partido ----------
partido = Partido(
    fecha=date(2024, 3, 17),
    equipo_local_id=equipo1.equipo_id,
    equipo_visitante_id=equipo2.equipo_id,
    goles_local=2,
    goles_visitante=1,
    temporada_id=temporada.temporada_id,
    competicion_id=competicion.competicion_id
)
session.add(partido)
session.commit()

# ---------- Crear estadísticas del partido ----------
estadisticas = EstadisticasPartido(
    partido_id=partido.partido_id,
    posesion_local=55,
    posesion_visitante=45,
    tiros_local=10,
    tiros_visitante=6,
    tiros_puerta_local=5,
    tiros_puerta_visitante=2,
    corners_local=4,
    corners_visitante=3,
    tarjetas_amarillas_local=1,
    tarjetas_amarillas_visitante=2,
    tarjetas_rojas_local=0,
    tarjetas_rojas_visitante=0
)
session.add(estadisticas)
session.commit()

# ---------- Comprobaciones ----------
print("\nEstadísticas del partido:")
print(f"Partido: {partido.equipo_local.nombre} vs {partido.equipo_visitante.nombre}")
print(f"Posesión: {partido.estadisticas.posesion_local}% - {partido.estadisticas.posesion_visitante}%")
print(f"Tiros: {partido.estadisticas.tiros_local} - {partido.estadisticas.tiros_visitante}")

# Comprobación inversa
print(f"\nEstadísticas asociadas al partido ID {estadisticas.partido_id}:")
print(f"Visitante: {estadisticas.partido.equipo_visitante.nombre}, Goles: {estadisticas.partido.goles_visitante}")

session.close()
