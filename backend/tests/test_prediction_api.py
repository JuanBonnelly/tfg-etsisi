# backend/tests/test_prediction_api.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import os
import numpy as np
from datetime import date, timedelta
from dotenv import load_dotenv
from unittest.mock import MagicMock, patch

# Importa la aplicación FastAPI y tus modelos ORM
from backend.main import app
from backend.dependencies import get_db_session, get_prediction_pipeline

from domain.models.base import Base
from domain.models.equipo import Equipo
from domain.models.partido import Partido
from domain.models.estadisticas_partido import EstadisticasPartido
from domain.models.competicion import Competicion
from domain.models.temporada import Temporada

# Cargar variables de entorno para la conexión a la DB de test
load_dotenv()

# --- Configuración para la base de datos de TEST en MySQL ---
TEST_DB_USER = os.getenv("TEST_DB_USER", os.getenv("DB_USER", "admin"))
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD", "admin"))
TEST_DB_HOST = os.getenv("TEST_DB_HOST", "localhost")
TEST_DB_PORT = os.getenv("TEST_DB_PORT", "3307")
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "futbol_tfg_test")

SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Override de la dependencia de sesión de DB para usar la DB de test ---
def override_get_db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db_session] = override_get_db_session

# --- Mocks para el modelo ML (inicialización segura al nivel del módulo) ---
mock_model_instance = MagicMock()
mock_scaler_instance = MagicMock()

# Configura los mocks para que se comporten como tu modelo espera.
mock_model_instance.classes_ = np.array([-1, 0, 1])
mock_model_instance.predict.return_value = np.array([1])
mock_model_instance.predict_proba.return_value = np.array([[0.1, 0.2, 0.7]])

# --- Fixtures de Pytest (DEBEN ESTAR DEFINIDAS AQUÍ, AL PRINCIPIO DEL MÓDULO) ---
@pytest.fixture(name="db_session_pred_test")
def db_session_pred_test_fixture():
    """
    Fixture de pytest que proporciona una sesión de base de datos MySQL limpia para cada test.
    TRUNCA todas las tablas relevantes antes de cada test.
    """
    db = TestingSessionLocal()
    try:
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        db.execute(text("TRUNCATE TABLE estadisticas_partido"))
        db.execute(text("TRUNCATE TABLE partido"))
        db.execute(text("TRUNCATE TABLE temporada"))
        db.execute(text("TRUNCATE TABLE competicion"))
        db.execute(text("TRUNCATE TABLE equipo"))
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_ml_mocks_globally():
    """
    Fixture que parchea las variables globales de modelo y scaler en dependencies.py
    para que apunten a los mocks, y simula la carga de artefactos ML.
    Se ejecuta automáticamente para todos los tests en este módulo.
    """
    with patch('backend.dependencies.ml_model', new=mock_model_instance), \
         patch('backend.dependencies.scaler', new=mock_scaler_instance), \
         patch('backend.dependencies.load_ml_artifacts', MagicMock(return_value=(mock_model_instance, mock_scaler_instance))):
        yield

@pytest.fixture # <--- ¡NUEVA FIXTURE PARA EL CLIENTE DE TEST!
def client():
    """
    Fixture que proporciona una instancia de TestClient para la aplicación FastAPI.
    Pytest inyectará esta instancia en cualquier función de test que la solicite.
    """
    return TestClient(app)

# --- Función auxiliar para cargar datos de prueba (NO ES UNA FIXTURE) ---
def setup_common_data(db_session: Session):
    """
    Carga datos comunes necesarios para la mayoría de los tests de predicción.
    Estos datos son suficientes para que las features se calculen (al menos sin NaNs).
    """
    # Competicion
    comp = Competicion(competicion_id=9, nombre="Premier League", abreviatura="PL")
    db_session.add(comp)
    db_session.commit()

    # Temporada
    temp = Temporada(temporada_id="2023-2024", año_inicio=2023, año_fin=2024, competicion_id=9)
    db_session.add(temp)
    db_session.commit()

    # Equipos
    team_arsenal = Equipo(equipo_id="ARS", nombre="Arsenal", abreviatura="ARS")
    team_spurs = Equipo(equipo_id="TOT", nombre="Tottenham", abreviatura="TOT")
    team_chelsea = Equipo(equipo_id="CHE", nombre="Chelsea", abreviatura="CHE")
    db_session.add_all([team_arsenal, team_spurs, team_chelsea])
    db_session.commit()

    # Generar datos históricos para que las features no sean todas NaN
    today = date.today()
    for i in range(1, 16):
        p = Partido(
            partido_id=f"P_ARS_{i}", fecha=today - timedelta(days=i*10),
            equipo_local_id="ARS", equipo_visitante_id="CHE" if i%2==0 else "TOT",
            goles_local=i%3 + 1, goles_visitante=(i+1)%3, temporada_id="2023-2024", competicion_id=9
        )
        ep = EstadisticasPartido(
            partido_id=f"P_ARS_{i}", posesion_local=50.0 + (i%5), posesion_visitante=50.0 - (i%5),
            corners_local=5 + i%2, corners_visitante=3 + i%3, tarjetas_amarillas_local=1,
            tarjetas_amarillas_visitante=1, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p, ep])

    for i in range(1, 16):
        p = Partido(
            partido_id=f"P_TOT_{i}", fecha=today - timedelta(days=i*10 + 5),
            equipo_local_id="TOT", equipo_visitante_id="CHE" if i%2!=0 else "ARS",
            goles_local=(i+1)%3 + 1, goles_visitante=i%3, temporada_id="2023-2024", competicion_id=9
        )
        ep = EstadisticasPartido(
            partido_id=f"P_TOT_{i}", posesion_local=45.0 + (i%5), posesion_visitante=55.0 - (i%5),
            corners_local=4 + i%2, corners_visitante=2 + i%3, tarjetas_amarillas_local=0,
            tarjetas_amarillas_visitante=2, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p, ep])
    
    for i in range(1, 11):
        p_h2h_ars = Partido(
            partido_id=f"H2H_ARS_TOT_{i}", fecha=today - timedelta(days=i*30 + 100),
            equipo_local_id="ARS", equipo_visitante_id="TOT",
            goles_local=2 + (i%2), goles_visitante=1 + (i%2), temporada_id="2023-2024", competicion_id=9
        )
        ep_h2h_ars = EstadisticasPartido(
            partido_id=f"H2H_ARS_TOT_{i}", posesion_local=55.0 + (i%3), posesion_visitante=45.0 - (i%3),
            corners_local=6, corners_visitante=2, tarjetas_amarillas_local=1,
            tarjetas_amarillas_visitante=1, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p_h2h_ars, ep_h2h_ars])

        p_h2h_tot = Partido(
            partido_id=f"H2H_TOT_ARS_{i}", fecha=today - timedelta(days=i*30 + 150),
            equipo_local_id="TOT", equipo_visitante_id="ARS",
            goles_local=1 + (i%2), goles_visitante=2 + (i%2), temporada_id="2023-2024", competicion_id=9
        )
        ep_h2h_tot = EstadisticasPartido(
            partido_id=f"H2H_TOT_ARS_{i}", posesion_local=40.0 + (i%3), posesion_visitante=60.0 - (i%3),
            corners_local=3, corners_visitante=5, tarjetas_amarillas_local=0,
            tarjetas_amarillas_visitante=2, tarjetas_rojas_local=0, tarjetas_rojas_visitante=0
        )
        db_session.add_all([p_h2h_tot, ep_h2h_tot])
        
    db_session.commit()


# --- Funciones de Test ---
def test_predict_match_success_mocked_ml_pipeline(client, db_session_pred_test: Session):
    """
    Test que mockea el pipeline ML (modelo y scaler) y permite
    que la lógica de cálculo de features se ejecute realmente.
    """
    mock_scaler_instance.transform.return_value = np.array([[0.5] * 47])

    setup_common_data(db_session_pred_test)

    request_body = {
        "local_team_name": "Arsenal",
        "visitor_team_name": "Tottenham",
        "match_date": "2024-05-15"
    }
    response = client.post("/predict", json=request_body)

    assert response.status_code == 200
    data = response.json()
    assert data["predicted_result"] == "Victoria Local"
    assert data["probabilities"]["Victoria Local"] == pytest.approx(0.7)
    assert data["probabilities"]["Empate"] == pytest.approx(0.2)
    assert data["probabilities"]["Victoria Visitante"] == pytest.approx(0.1)

    mock_model_instance.predict.assert_called_once()
    mock_scaler_instance.transform.assert_called_once()


def test_predict_match_team_not_found(client, db_session_pred_test: Session):
    """
    Test que verifica el manejo de error cuando un equipo no se encuentra.
    """
    setup_common_data(db_session_pred_test)

    request_body = {
        "local_team_name": "EquipoInexistente",
        "visitor_team_name": "Tottenham",
        "match_date": "2024-05-15"
    }
    response = client.post("/predict", json=request_body)
    assert response.status_code == 400
    assert "Equipo local 'EquipoInexistente' no encontrado." in response.json()["detail"]


def test_predict_match_insufficient_historical_data(client, db_session_pred_test: Session):
    """
    Test que verifica el comportamiento de la API cuando no hay suficientes datos históricos
    para calcular las features (ej. equipos nuevos o partidos muy antiguos).
    Según la Opción A, la API debe devolver 200 OK y una predicción (basada en features imputadas a 0).
    """
    # 1. Preparar datos mínimos: solo añadir los equipos, sin historial de partidos.
    team_new = Equipo(equipo_id="NEW", nombre="Equipo Nuevo", abreviatura="NEW")
    team_old = Equipo(equipo_id="OLD", nombre="Equipo Viejo", abreviatura="OLD")
    db_session_pred_test.add_all([team_new, team_old])
    db_session_pred_test.commit()

    # 2. Definir el cuerpo de la solicitud
    request_body = {
        "local_team_name": "Equipo Nuevo",
        "visitor_team_name": "Equipo Viejo",
        "match_date": "2024-05-15"
    }

    # 3. Realizar la solicitud a la API
    response = client.post("/predict", json=request_body)

    # 4. Asertar el comportamiento esperado (según Opción A: 200 OK)
    assert response.status_code == 200 # <--- ¡CAMBIO CRUCIAL AQUÍ!
    
    # Opcional: También puedes verificar el contenido de la respuesta si es relevante
    data = response.json()
    assert "predicted_result" in data
    assert "probabilities" in data
    # Si sabes qué predicción da tu modelo para un vector de ceros, puedes asertarla aquí.
    # Por ejemplo, si un vector de ceros siempre predice "Empate" con 0.5 de prob:
    # assert data["predicted_result"] == "Empate"
    # assert data["probabilities"]["Empate"] == pytest.approx(0.5)