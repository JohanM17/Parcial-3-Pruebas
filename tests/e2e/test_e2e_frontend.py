"""
Punto 4: Automatizacion Frontend E2E — TicketFast
Archivo: tests/e2e/test_e2e_frontend.py

Herramienta elegida: Playwright (Python)
Frontend en: http://localhost:4200/reservas

Flujo automatizado:
  1. Navegar a la URL de reservas.
  2. Diligenciar el formulario: correo, zona VIP, cantidad 1.
  3. Hacer clic en el boton de confirmacion.
  4. Verificar (con espera dinamica nativa de Playwright) que el elemento
     seccion-resumen-total contenga el texto "150.000".

Regla de negocio: VIP (150.000 COP) x 1 asiento = 150.000 COP
"""

from playwright.sync_api import Page, expect


def test_reserva_vip_muestra_total_en_resumen(page: Page):
    """
    Prueba E2E que valida el flujo completo de reserva desde el frontend:
    - Llena el formulario con zona VIP y cantidad 1.
    - Confirma la reserva.
    - Verifica que el total mostrado sea 150.000 COP.
    No usa sleep: utiliza las esperas dinamicas nativas de Playwright (expect).
    """
    # Paso 1: navegar a la interfaz de reservas
    page.goto("http://localhost:4200/reservas")

    # Paso 2: diligenciar el formulario
    page.get_by_test_id("input-email-cliente").fill("cliente@ticketfast.com")
    page.get_by_test_id("select-zona-evento").select_option("VIP")
    page.get_by_test_id("input-cantidad-asientos").fill("1")

    # Paso 3: hacer clic en el boton de confirmacion
    page.get_by_test_id("btn-confirmar-reserva").click()

    # Paso 4: verificar con espera dinamica que el resumen muestre "150.000"
    # expect() espera automaticamente hasta que la condicion se cumpla (sin sleep)
    resumen = page.get_by_test_id("seccion-resumen-total")
    expect(resumen).to_contain_text("150.000")
