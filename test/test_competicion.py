import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.competicion import Competicion
from domain.models.temporada import Temporada
from domain.models.partido import Partido
from domain.models.equipo import Equipo

# Crear las tablas
Base.metadata.create_all(get_engine())

session = get_session()

# ---------- Crear equipos ----------
equipo1 = Equipo(nombre="Real Madrid", abreviatura="RMA")
equipo2 = Equipo(nombre="Atlético", abreviatura="ATM")
session.add_all([equipo1, equipo2])
session.commit()

# ---------- Crear competición ----------
competicion = Competicion(nombre="LaLiga", abreviatura="LL")
session.add(competicion)
session.commit()

# ---------- Crear temporada asociada a competición ----------
temporada = Temporada(
    año_inicio=2023,
    año_fin=2024,
    competicion_id=competicion.competicion_id
)
session.add(temporada)
session.commit()

# ---------- Crear partido asociado a temporada y competición ----------
partido = Partido(
    fecha=date(2024, 1, 20),
    equipo_local_id=equipo1.equipo_id,
    equipo_visitante_id=equipo2.equipo_id,
    goles_local=1,
    goles_visitante=1,
    temporada_id=temporada.temporada_id,
    competicion_id=competicion.competicion_id
)
session.add(partido)
session.commit()

# ---------- Comprobar relación Competición → Temporadas ----------
print("\nTemporadas asociadas a la competición LaLiga:")
for t in competicion.temporadas:
    print(f"- {t.año_inicio}-{t.año_fin}")

# ---------- Comprobar relación Temporada → Partidos ----------
print(f"\nPartidos registrados en la temporada {temporada.año_inicio}-{temporada.año_fin}:")
for p in temporada.partidos:
    print(f"{p.fecha} - {p.equipo_local.nombre} vs {p.equipo_visitante.nombre} → {p.goles_local}:{p.goles_visitante}")

session.close()
