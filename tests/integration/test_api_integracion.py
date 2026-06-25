"""
Punto 2: Prueba de Integracion de API — TicketFast
Archivo: tests/integration/test_api_integracion.py

Valida que el endpoint POST /reservas/{evento_id} persiste correctamente
un registro en la base de datos y retorna HTTP 201.
"""

from src.database.models import ReservaDB


def test_crear_reserva_retorna_201_y_persiste_en_bd(client_con_bd, db_session):
    """
    Prueba de integracion:
    1. Realiza una peticion POST al endpoint /reservas/concierto-2026
       con un payload valido.
    2. Verifica que el codigo de estado HTTP sea 201 (Created).
    3. Consulta directamente la base de datos mediante SQLAlchemy y verifica
       que el registro ReservaDB exista y que el campo cliente_email
       coincida con el valor enviado en la peticion.
    """
    payload = {
        "cliente_email": "test@correo.com",
        "zona": "VIP",
        "cantidad": 2,
    }

    # Peticion HTTP al endpoint
    response = client_con_bd.post("/reservas/concierto-2026", json=payload)

    # Asercion 1: el codigo de estado debe ser 201 Created
    assert response.status_code == 201

    # Asercion 2: el registro debe existir en la base de datos
    reserva_en_bd = (
        db_session.query(ReservaDB)
        .filter(ReservaDB.evento_id == "concierto-2026")
        .first()
    )
    assert reserva_en_bd is not None
    assert reserva_en_bd.cliente_email == "test@correo.com"
