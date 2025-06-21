import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.database.mysql_connect import get_engine
from domain.models.competicion import Competicion
from domain.models.equipo import Equipo
from domain.models.temporada import Temporada
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido


# Obtener la clase Base desde cualquiera de los modelos (todos heredan la misma)
Base = Competicion.__bases__[0]

# Crear el engine usando la configuración del .env
engine = get_engine()

# Crear todas las tablas en la base de datos apuntada por el engine
Base.metadata.create_all(engine)

print("✔ Tablas creadas correctamente en la base seleccionada.")
