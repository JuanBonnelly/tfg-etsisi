import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.database.mysql_connect import get_session
from scraper.scraper_estadisticas import scrape_estadisticas
from domain.models.estadisticas_partido import EstadisticasPartido

# Crear sesión
session = get_session()

# Forzar prueba con partido_id conocido
partido_id = "3adf2aa7"
estadisticas = scrape_estadisticas(partido_id)

if estadisticas:
    # Guardar en base de datos
    session.add(estadisticas)
    session.commit()
    print(f"\n Estadísticas insertadas para el partido {partido_id}")
else:
    print(f"\n No se encontraron estadísticas para el partido {partido_id}")

# Mostrar resultado guardado
resultado = session.query(EstadisticasPartido).filter_by(partido_id=partido_id).first()
if resultado:
    print("\n Estadísticas recuperadas de la base de datos:")
    print(f"Partido ID: {resultado.partido_id}")
    print(f"Posesión: {resultado.posesion_local} - {resultado.posesion_visitante}")
    print(f"Tiros: {resultado.tiros_local} - {resultado.tiros_visitante}")
    print(f"Corners: {resultado.corners_local} - {resultado.corners_visitante}")
else:
    print("\n No se encontraron estadísticas en la base de datos.")

session.close()
