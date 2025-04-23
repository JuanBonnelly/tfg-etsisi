import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.partido import Partido
from domain.models.equipo import Equipo
from scraper.scraper_partido import scrape_partidos
from domain.models.temporada import Temporada
from domain.models.competicion import Competicion



# 1. Inicializar la base de datos (crea las tablas si no existen)
engine = get_engine()
Base.metadata.create_all(engine)

# 2. Crear una nueva sesión
session = get_session()

# 3. Ejecutar el scraper de partidos
partidos, equipos = scrape_partidos()

# 4. Insertar equipos sin duplicados
for equipo in equipos:
    if not session.query(Equipo).filter_by(equipo_id=equipo.equipo_id).first():
        session.add(equipo)
session.commit()

# 5. Insertar partidos
session.add_all(partidos)
session.commit()

# 6. Comprobación
print("\n Partidos insertados:")
for p in session.query(Partido).all():
    print(f"{p.fecha}: {p.equipo_local_id} vs {p.equipo_visitante_id} - {p.goles_local}:{p.goles_visitante}")

print("\n Equipos insertados:")
for e in session.query(Equipo).all():
    print(f"{e.equipo_id}: {e.nombre} ({e.abreviatura})")

session.close()
