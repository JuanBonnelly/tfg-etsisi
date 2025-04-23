import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date
from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.temporada import Temporada
from domain.models.partido import Partido
from domain.models.equipo import Equipo

# Comentado hasta que se implemente la clase Competicion
# from domain.models.competicion import Competicion

# Crear tablas
Base.metadata.create_all(get_engine())

session = get_session()

# ---------- Crear equipos ----------
equipo1 = Equipo(nombre="Sevilla", abreviatura="SEV")
equipo2 = Equipo(nombre="Barcelona", abreviatura="FCB")
session.add_all([equipo1, equipo2])
session.commit()

# ---------- Crear una temporada ----------
temporada = Temporada(
    año_inicio=2022,
    año_fin=2023,
    competicion_id=2021  #  Temporal hasta que se cree Competicion
)
session.add(temporada)
session.commit()

# ---------- Crear partidos asociados a la temporada ----------
partido1 = Partido(
    fecha=date(2023, 2, 15),
    equipo_local_id=equipo1.equipo_id,
    equipo_visitante_id=equipo2.equipo_id,
    goles_local=1,
    goles_visitante=3,
    temporada_id=temporada.temporada_id,
    competicion_id=1  #  Temporal
)

partido2 = Partido(
    fecha=date(2023, 5, 10),
    equipo_local_id=equipo2.equipo_id,
    equipo_visitante_id=equipo1.equipo_id,
    goles_local=2,
    goles_visitante=2,
    temporada_id=temporada.temporada_id,
    competicion_id=1  #  Temporal
)

session.add_all([partido1, partido2])
session.commit()

# ---------- Verificar relación desde Partido → Temporada ----------
print("\n Temporada asociada a un partido:")
print(f"{partido1} pertenece a la temporada {partido1.temporada.año_inicio}-{partido1.temporada.año_fin}")

# ---------- Verificar relación desde Temporada → Partidos ----------
print("\n Partidos registrados en la temporada 2022-2023:")
for p in temporada.partidos:
    print(f"{p.fecha} - {p.equipo_local.nombre} vs {p.equipo_visitante.nombre} → {p.goles_local}:{p.goles_visitante}")

session.close()
