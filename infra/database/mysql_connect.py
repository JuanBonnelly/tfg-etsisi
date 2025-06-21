import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv # <--- ¡DESCOMENTADA!

# Cargar las variables desde el .env
# Por defecto, load_dotenv() NO SOBRESCRITBE variables de entorno ya existentes.
# Esto significa que las variables de Docker Compose (DB_HOST=db, DB_PORT=3306)
# tendrán prioridad cuando se ejecute dentro del contenedor.
# Pero cuando se ejecute LOCALMENTE (fuera de Docker), leerá del .env.
load_dotenv()

# Cargar el .env forzando la sobreescritura de variables existentes
#load_dotenv(override=True)

# Leer credenciales desde variables de entorno
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")  # cuidado: aquí usas DB_PASSWORD, no DB_PASS como antes
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Comprobación adicional (para debug)
print(f"USANDO CREDENCIALES: user={user}, password={password}, host={host}, port={port}, database={database}")

# Crear el engine y el sessionmaker a nivel global
url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(url)
Session = sessionmaker(bind=engine)

# Funciones accesibles desde otros módulos
def get_engine():
    return engine

def get_session():
    return Session()
