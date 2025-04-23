import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.competicion import Competicion
from domain.models.temporada import Temporada
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido

# Crear tablas
Base.metadata.create_all(get_engine())
session = get_session()

# ---------- Crear entidades base ----------
equipo1 = Equipo(equipo_id="GIR123", nombre="Girona", abreviatura="GIR")

equipo2 = Equipo(equipo_id="AS", nombre="Arsenal", abreviatura="AS")

competicion = Competicion(nombre="LaLiga", abreviatura="LL")
session.add_all([equipo1, equipo2, competicion])
session.commit()

# ---------- Crear temporada asociada a competición ----------
temporada = Temporada(año_inicio=2023, año_fin=2024, competicion_id=competicion.competicion_id)
session.add(temporada)
session.commit()

# ---------- Crear partido ----------
partido = Partido(
    fecha=date(2024, 4, 10),
    equipo_local_id=equipo1.equipo_id,
    equipo_visitante_id=equipo2.equipo_id,
    goles_local=2,
    goles_visitante=1,
    temporada_id=temporada.temporada_id,
    competicion_id=competicion.competicion_id
)
session.add(partido)
session.commit()

# ---------- Añadir estadísticas ----------
estadisticas = EstadisticasPartido(
    partido_id=partido.partido_id,
    posesion_local=53.0,
    posesion_visitante=47.0,
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

# ---------- Validaciones de relaciones ----------
print("\n VALIDACIÓN COMPLETA DEL MODELO DE DATOS\n")

# Partido → Equipos
print(f"Partido: {partido.equipo_local_id} vs {partido.equipo_visitante_id}")
print(f"Resultado: {partido.goles_local} - {partido.goles_visitante}")

# Partido → Temporada / Competición
print(f"Temporada: {partido.temporada.año_inicio}-{partido.temporada.año_fin}")
print(f"Competición: {partido.competicion.nombre}")

# Partido → Estadísticas
print(f"Posesión: {partido.estadisticas.posesion_local}% - {partido.estadisticas.posesion_visitante}%")
print(f"Tiros: {partido.estadisticas.tiros_local} - {partido.estadisticas.tiros_visitante}")

# Estadísticas → Partido (relación inversa)
print(f"\nEstadísticas enlazadas al partido: {estadisticas.partido.equipo_local.nombre} vs {estadisticas.partido.equipo_visitante.nombre}")

# Temporada → Partidos (inversa)
print(f"\nPartidos en la temporada {temporada.año_inicio}-{temporada.año_fin}:")
for p in temporada.partidos:
    print(f"- {p.fecha} → {p.equipo_local.nombre} vs {p.equipo_visitante.nombre}")

# Competición → Temporadas (inversa)
print(f"\nTemporadas en la competición {competicion.nombre}:")
for t in competicion.temporadas:
    print(f"- {t.año_inicio}-{t.año_fin}")

# Equipo → Partidos como local o visitante (doble filtro)
partidos_equipo1 = session.query(Partido).filter(
    (Partido.equipo_local_id == equipo1.equipo_id) |
    (Partido.equipo_visitante_id == equipo1.equipo_id)
).all()

print(f"\nPartidos del equipo {equipo1.nombre}:")
for p in partidos_equipo1:
    print(f"- {p.fecha}: {p.equipo_local.nombre} vs {p.equipo_visitante.nombre} ({p.goles_local}:{p.goles_visitante})")

session.close()
