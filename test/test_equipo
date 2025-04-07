import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from infra.database.mysql_connect import get_engine, get_session
from domain.models.base import Base
from domain.models.equipo import Equipo

# Paso 1: Crear las tablas si aún no existen
# Esto lee todas las clases que heredan de Base y crea las tablas correspondientes en la BD
Base.metadata.create_all(get_engine())

# Paso 2: Obtener una sesión para interactuar con la base de datos
session = get_session()

# Paso 3: Crear un nuevo objeto Equipo
nuevo_equipo = Equipo(nombre="Atlético de Madrid", abreviatura="ATM")

# Paso 4: Añadir el objeto a la sesión y guardar los cambios (commit)
session.add(nuevo_equipo)
session.commit()

# Paso 5: Consultar todos los equipos en la base de datos y mostrarlos por consola
equipos = session.query(Equipo).all()
print("\nEquipos en la base de datos:")
for equipo in equipos:
    print(equipo)

# Paso 6: Cerrar la sesión (buena práctica)
session.close()
