import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from infra.database.mysql_connect import get_session

def truncar_tablas():
    session = get_session()

    try:
        print("\n Desactivando claves foráneas...")
        session.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        tablas = [
            "estadisticas_partido",
            "partido",
            "equipo",
            "temporada",
            "competicion"
        ]

        for tabla in tablas:
            print(f" Limpiando tabla: {tabla}")
            session.execute(text(f"TRUNCATE TABLE {tabla};"))

        print(" Tablas limpiadas correctamente.")
    finally:
        print(" Reactivando claves foráneas...")
        session.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
        session.commit()
        session.close()

if __name__ == "__main__":
    truncar_tablas()
