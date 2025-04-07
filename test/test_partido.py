import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import date

from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.partido import Partido

# Temporales (comentar hasta que estén implementados)
# from domain.models.temporada import Temporada
# from domain.models.competicion import Competicion

# Crear las tablas si no existen
Base.metadata.create_all(get_engine())

# Crear sesión
session = get_session()

# ---------- 1. Crear datos auxiliares ----------

equipo_local = Equipo(nombre="Valencia CF", abreviatura="VAL")
equipo_visitante = Equipo(nombre="Villarreal", abreviatura="VIL")

# TODO: crear temporada y competición cuando se implementen
# temporada = Temporada(año_inicio=2023, año_fin=2024)
# competicion = Competicion(nombre="La Liga", abreviatura="LL")

session.add_all([equipo_local, equipo_visitante])
session.commit()

# ---------- 2. Crear un partido ----------

partido = Partido(
    fecha=date(2024, 5, 15),
    equipo_local_id=equipo_local.equipo_id,
    equipo_visitante_id=equipo_visitante.equipo_id,
    goles_local=2,
    goles_visitante=2,
    temporada_id=1,      #  Temporal hasta que tengamos la clase Temporada
    competicion_id=1     #  Temporal hasta que tengamos la clase Competicion
)

session.add(partido)
session.commit()

# ---------- 3. Comprobar que el partido existe ----------

partidos = session.query(Partido).all()
print("\n Lista de partidos registrados:")
for p in partidos:
    print(p)

# ---------- 4. Comprobar las relaciones ORM ----------

print("\n Comprobando relación con Equipos:")
for p in partidos:
    print(f"{p.equipo_local.nombre} vs {p.equipo_visitante.nombre} - {p.goles_local}:{p.goles_visitante}")


# ---------- 5. Comprobar relación inversa desde Equipo ----------
print("\n✅ Comprobando relación inversa desde Equipo:")

valencia = session.query(Equipo).filter_by(nombre="Valencia CF").first()
for p in valencia.partidos_local:
    print(f"Valencia jugó como local contra {p.equipo_visitante.nombre} el {p.fecha}")


session.close()
