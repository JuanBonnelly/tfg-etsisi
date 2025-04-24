import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.temporada import Temporada
from domain.models.competicion import Competicion
from scraper.scraper_temporada import scrape_temporadas

# 1. Inicializar la base de datos (crea las tablas si no existen)
engine = get_engine()
Base.metadata.create_all(engine)

# 2. Crear una nueva sesión
session = get_session()

# 3. Ejecutar el scraper de temporadas y competiciones
temporadas, competiciones = scrape_temporadas()

# 4. Insertar competiciones sin duplicados
for comp in competiciones:
    if not session.query(Competicion).filter_by(competicion_id=comp.competicion_id).first():
        print(f" Insertando competición: {comp.nombre}")
        session.add(comp)
session.commit()

# 5. Insertar temporadas sin duplicados
for temp in temporadas:
    if not session.query(Temporada).filter_by(temporada_id=temp.temporada_id).first():
        print(f" Insertando temporada: {temp.temporada_id} ({temp.año_inicio}-{temp.año_fin})")
        session.add(temp)
session.commit()

# 6. Comprobación
print("\n Temporadas insertadas:")
for t in session.query(Temporada).order_by(Temporada.temporada_id.desc()).all():
    print(f"{t.temporada_id}: {t.año_inicio}-{t.año_fin} | Comp: {t.competicion_id}")

print("\n Competiciones insertadas:")
for c in session.query(Competicion).all():
    print(f"{c.competicion_id}: {c.nombre} ({c.abreviatura})")

session.close()
