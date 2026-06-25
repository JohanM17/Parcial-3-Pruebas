"""
Punto 3: Prueba de Sistema E2E — TicketFast
Archivo: tests/system/test_sistema_e2e.py

Prueba de sistema: NO usa fixtures de BD ni conoce el codigo interno.
Realiza peticiones HTTP reales contra el servicio levantado en contenedores
(api-test corriendo en http://localhost:8001).

Regla de negocio validada:
  - Zona General: 50.000 COP por asiento
  - Cantidad 3 asientos → total_recaudado esperado: 150.000 COP
"""

import httpx

BASE_URL = "http://localhost:8001"
EVENTO_ID = "sistema-evento-xyz"


def test_flujo_completo_reserva_y_calculo_financiero():
    """
    Prueba de sistema que valida el flujo completo:
    1. POST real para crear una reserva en zona General con cantidad 3.
    2. GET real al endpoint de resumen del evento.
    3. Assert que total_recaudado == 150000 (3 asientos x 50.000 COP).
    """
    payload = {
        "cliente_email": "sistema@test.com",
        "zona": "General",
        "cantidad": 3,
    }

    # Paso 1: crear la reserva via peticion HTTP real
    respuesta_post = httpx.post(
        f"{BASE_URL}/reservas/{EVENTO_ID}",
        json=payload,
    )
    assert respuesta_post.status_code == 201

    # Paso 2: consultar el resumen financiero del evento via GET real
    respuesta_get = httpx.get(f"{BASE_URL}/reservas/{EVENTO_ID}/resumen")
    assert respuesta_get.status_code == 200

    # Paso 3: validar el calculo de la regla de negocio
    # General (50.000 COP) x 3 asientos = 150.000 COP
    datos = respuesta_get.json()
    assert datos["total_recaudado"] == 150000
