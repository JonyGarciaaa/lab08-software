"""NIVEL DE SISTEMA (E2E) — Playwright en un navegador real.

Objeto de prueba: los flujos del usuario en la interfaz web.
La fixture `page` la provee pytest-playwright; las rutas relativas usan base_url.
Los datos se reinician antes de cada prueba.

Ejecuta solo este nivel:          pytest tests/e2e -v
Para VER el navegador:            pytest tests/e2e --headed --slowmo 500
Para grabar interacciones:        playwright codegen http://127.0.0.1:5000
                                  (con la app corriendo: python run.py)
"""
import re
from playwright.sync_api import Page, expect


def iniciar_sesion(page: Page, usuario="admin", password="Admin123"):
    page.goto("/login")
    page.get_by_label("Usuario").fill(usuario)
    page.get_by_label("Contraseña").fill(password)
    page.get_by_role("button", name="Ingresar").click()


# ---------------------------------------------------------------- EJEMPLO
def test_pagina_de_login_carga(page: Page):
    page.goto("/login")
    expect(page.get_by_role("heading", name="Iniciar sesión")).to_be_visible()


# ---------------------------------------------------------------- PRUEBAS E2E

def test_acceso_sin_sesion_redirige_a_login(page: Page):
    page.goto("/productos")
    expect(page).to_have_url(re.compile(r"/login"))


def test_login_exitoso_muestra_bienvenida(page: Page):
    iniciar_sesion(page, "admin", "Admin123")
    expect(page).to_have_url(re.compile(r"/productos"))
    expect(page.locator("#bienvenida")).to_contain_text("Bienvenido, admin")


def test_login_fallido_muestra_error(page: Page):
    iniciar_sesion(page, "admin", "PasswordIncorrecta")
    expect(page.get_by_text("Usuario o contraseña incorrectos")).to_be_visible()


def test_crear_producto_formulario_y_tabla(page: Page):
    iniciar_sesion(page)
    page.get_by_role("link", name="Nuevo producto").click()
    page.get_by_label("Nombre").fill("Webcam HD")
    page.get_by_label("Precio").fill("350.00")
    page.get_by_label("Stock").fill("8")
    page.get_by_role("button", name="Guardar").click()

    expect(page).to_have_url(re.compile(r"/productos"))
    expect(page.get_by_text("Producto creado")).to_be_visible()
    
    fila_nueva = page.get_by_role("row").filter(has_text="Webcam HD")
    expect(fila_nueva).to_be_visible()
    expect(fila_nueva).to_contain_text("350.00")
    expect(fila_nueva).to_contain_text("8")


def test_editar_producto_muestra_mensaje_y_actualiza_tabla(page: Page):
    iniciar_sesion(page)
    page.get_by_role("row").filter(has_text="Monitor").get_by_role("link", name="Editar").click()
    page.get_by_label("Nombre").fill("Monitor 27 pulgadas")
    page.get_by_label("Precio").fill("1999.99")
    page.get_by_label("Stock").fill("3")
    page.get_by_role("button", name="Guardar").click()

    expect(page.get_by_text("Producto actualizado")).to_be_visible()
    fila = page.get_by_role("row").filter(has_text="Monitor 27 pulgadas")
    expect(fila).to_contain_text("1999.99")
    expect(fila).to_contain_text("3")


def test_eliminar_producto_especifico_sin_efectos_colaterales(page: Page):
    # Regla: "Eliminar" borra ese producto, muestra "Producto eliminado" y los demás productos no cambian.
    # Detecta DEF-03: en productos.html siempre se envía eliminar pid=productos[0].id (borra Teclado en vez de Mouse).
    iniciar_sesion(page)
    
    # Intentar eliminar el segundo producto ("Mouse")
    fila_mouse = page.get_by_role("row").filter(has_text="Mouse")
    expect(fila_mouse).to_be_visible()
    fila_mouse.get_by_role("button", name="Eliminar").click()

    expect(page.get_by_text("Producto eliminado")).to_be_visible()
    
    # Verificación del oráculo: Mouse ya NO debe existir en la tabla
    expect(page.get_by_role("row").filter(has_text="Mouse")).not_to_be_visible()
    
    # Efecto colateral: Teclado debería seguir existiendo intacto
    expect(page.get_by_role("row").filter(has_text="Teclado")).to_be_visible()
