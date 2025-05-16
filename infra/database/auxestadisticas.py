import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sqlalchemy import text
from infra.database.mysql_connect import get_session
import csv


def insertar_estadisticas_csv():
    session = get_session()

    with open("data/datosFbref/fbref_stats_202505141135.csv", newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            insert_query = text("""
                INSERT INTO estadisticas_partido_csv (
                    partido_id, equipo_id, posesion, corners, amarillas, rojas
                ) VALUES (:partido_id, :equipo_id, :posesion, :corners, :amarillas, :rojas)
            """)
            session.execute(insert_query, {
                'partido_id': row["match_id"],
                'equipo_id': row["team_id"],
                'posesion': float(row["team_match_possession"] or 0),
                'corners': int(row["team_match_corners"] or 0),
                'amarillas': int(row["team_match_yellow_cards"] or 0),
                'rojas': int(row["team_match_red_cards"] or 0)
            })

    session.commit()
    session.close()
    print("✅ Datos insertados en estadisticas_partido_csv con SQLAlchemy.")

if __name__ == "__main__":
    insertar_estadisticas_csv()
