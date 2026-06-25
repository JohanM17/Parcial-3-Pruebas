"""
conftest.py — Fixtures de prueba para TicketFast.

Configurado de manera identica al repositorio de clase carrito-compras.
Proporciona:
  - db_session: sesion SQLAlchemy con aislamiento por transaccion + rollback automatico.
  - client_con_bd: TestClient de FastAPI con la sesion de pruebas inyectada via override.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database.models import Base
from src.reservas.api import app
from src.database.config import get_db

# Base de datos SQLite en memoria para pruebas de integracion
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ticketfast.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """
    Fixture que crea todas las tablas, abre una conexion con una transaccion
    anidada y hace rollback al finalizar cada prueba para garantizar aislamiento.
    """
    Base.metadata.create_all(bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client_con_bd(db_session):
    """
    Fixture que sobreescribe la dependencia get_db de FastAPI con la sesion
    de prueba y devuelve un TestClient listo para usar.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
