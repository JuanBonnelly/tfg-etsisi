# backend/tests/test_teams_api.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Importa la aplicación FastAPI y tus modelos ORM
from backend.main import app
from backend.dependencies import get_db_session
from domain.models.base import Base # Necesario para crear/dropear tablas
from domain.models.equipo import Equipo # Modelo que vamos a testear

# Cargar variables de entorno para la conexión a la DB de test
load_dotenv()

# --- Configuración para la base de datos de TEST en MySQL ---
# Usaremos una base de datos MySQL específica para tests para aislar los datos.
# Estas variables se leerán de .env o del entorno del Docker Compose si lo configuras
TEST_DB_USER = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "admin"))
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD", "admin"))
TEST_DB_HOST = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST", "localhost"))
TEST_DB_PORT = os.getenv("TEST_DB_PORT", os.getenv("DB_PORT", "3307")) # Usar el puerto mapeado por Docker Compose
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "futbol_tfg_test") # Nombre de la DB de test

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)

# Crea un engine y sessionmaker para la DB de test
# Es crucial que la DB `futbol_tfg_test` exista en tu servidor MySQL.
# Puedes crearla manualmente o añadir un script para ello.
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Override de la dependencia de sesión de DB para usar la DB de test ---
def override_get_db_session():
    """
    Dependencia que proporciona una sesión de DB para los tests, conectándose a MySQL de test.
    """
    db = TestingSessionLocal()
    try:
        yield db # El test se ejecuta aquí
    finally:
        db.close()

# Aplica el override a la dependencia global de FastAPI
app.dependency_overrides[get_db_session] = override_get_db_session

# Cliente de test para la aplicación FastAPI
client = TestClient(app)

@pytest.fixture(name="db_session_test")
def db_session_test_fixture():
    """
    Fixture de pytest que proporciona una sesión de base de datos limpia para cada test.
    TRUNCA las tablas y carga datos mínimos.
    """
    db = TestingSessionLocal()
    try:
        # Limpiar tablas antes de cada test (¡cuidado con la tabla de producción!)
        # Es importante TRUNCATE y no DROP_ALL/CREATE_ALL si quieres reusar la DB.
        # Asegúrate de que tu DB de test (`futbol_tfg_test`) solo tenga las tablas necesarias.
        db.execute("TRUNCATE TABLE equipo") # Limpia la tabla equipo
        db.commit() # Commit de la limpieza

        yield db # El test se ejecuta aquí

        # Opcional: limpiar de nuevo al final, pero TRUNCATE al inicio suele ser suficiente
        # db.execute("TRUNCATE TABLE equipo")
        # db.commit()
    finally:
        db.close()

def test_get_teams_empty(db_session_test: Session):
    """
    Verifica que el endpoint /teams retorna una lista vacía si no hay equipos.
    """
    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == []

def test_get_teams_with_data(db_session_test: Session):
    """
    Verifica que el endpoint /teams retorna los equipos correctamente.
    """
    # Insertar algunos equipos de prueba directamente en la DB de test
    team1 = Equipo(equipo_id="FCB", nombre="FC Barcelona", abreviatura="BAR")
    team2 = Equipo(equipo_id="RMA", nombre="Real Madrid", abreviatura="RMA")
    team3 = Equipo(equipo_id="ATM", nombre="Atlético de Madrid", abreviatura="ATM")
    db_session_test.add(team1)
    db_session_test.add(team2)
    db_session_test.add(team3)
    db_session_test.commit()

    response = client.get("/teams")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

    # Verificar que los datos se devuelven correctamente y ordenados por nombre
    expected_names = ["Atlético de Madrid", "FC Barcelona", "Real Madrid"]
    actual_names = [t["name"] for t in data]
    assert actual_names == expected_names

    assert data[0]["team_id"] == "ATM"
    assert data[0]["abreviatura"] == "ATM"