import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar las variables desde el .env
load_dotenv()

# Leer credenciales desde variables de entorno
user = os.getenv("DB_USER")
password = os.getenv("DB_PASS")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

# Crear el engine y el sessionmaker a nivel global
url = f"mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(url)
Session = sessionmaker(bind=engine)

# Funciones accesibles desde otros módulos
def get_engine():
    return engine

def get_session():
    return Session()
