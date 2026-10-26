"""NIVEL DE INTEGRACIÓN (API) — Playwright APIRequestContext.

Objeto de prueba: el contrato HTTP de /api/... (rutas, códigos de estado, JSON).
Fixtures disponibles (ver tests/conftest.py):
    api               -> cliente sin token
    api_autenticada   -> cliente con token válido
Los datos se reinician antes de cada prueba (3 productos iniciales, ids 1, 2 y 3).

Ejecuta solo este nivel:   pytest tests/api -v
"""
import pytest


# ---------------------------------------------------------------- EJEMPLO
def test_listar_productos_devuelve_los_tres_iniciales(api_autenticada):
    respuesta = api_autenticada.get("/api/productos")
    assert respuesta.status == 200
    assert len(respuesta.json()) == 3


# ---------------------------------------------------------------- PRUEBAS DE API

# 1. Login (/api/login)
def test_login_credenciales_correctas(api):
    respuesta = api.post("/api/login", data={"usuario": "admin", "password": "Admin123"})
    assert respuesta.status == 200
    cuerpo = respuesta.json()
    assert "token" in cuerpo
    assert isinstance(cuerpo["token"], str) and len(cuerpo["token"]) > 0


def test_login_credenciales_incorrectas(api):
    respuesta = api.post("/api/login", data={"usuario": "admin", "password": "PasswordIncorrecto1"})
    assert respuesta.status == 401


def test_login_formato_invalido(api):
    respuesta = api.post("/api/login", data={"usuario": "", "password": "123"})
    assert respuesta.status == 400
    cuerpo = respuesta.json()
    assert "errores" in cuerpo
    assert len(cuerpo["errores"]) > 0



@pytest.mark.parametrize("metodo, ruta", [
    ("get", "/api/productos"),
    ("post", "/api/productos"),
    ("get", "/api/productos/1"),
    ("put", "/api/productos/1"),
    ("delete", "/api/productos/1"),
])
def test_rutas_protegidas_sin_token_responden_401(api, metodo, ruta):
    llamada = getattr(api, metodo)
    respuesta = llamada(ruta)
    assert respuesta.status == 401



def test_crear_producto_valido(api_autenticada):
    datos = {"nombre": "Audífonos Gamer", "precio": 199.99, "stock": 15}
    respuesta = api_autenticada.post("/api/productos", data=datos)
    assert respuesta.status == 201
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 4
    assert cuerpo["nombre"] == "Audífonos Gamer"
    assert cuerpo["precio"] == 199.99
    assert cuerpo["stock"] == 15


def test_obtener_producto_existente(api_autenticada):
    respuesta = api_autenticada.get("/api/productos/1")
    assert respuesta.status == 200
    cuerpo = respuesta.json()
    assert cuerpo["id"] == 1
    assert cuerpo["nombre"] == "Teclado"


def test_actualizar_producto_valido(api_autenticada):
    datos = {"nombre": "Teclado Mecánico RGB", "precio": 350.00, "stock": 8}
    respuesta = api_autenticada.put("/api/productos/1", data=datos)
    assert respuesta.status == 200
    cuerpo = respuesta.json()
    assert cuerpo["nombre"] == "Teclado Mecánico RGB"
    assert cuerpo["precio"] == 350.00
    assert cuerpo["stock"] == 8


def test_eliminar_producto_existente(api_autenticada):
    respuesta = api_autenticada.delete("/api/productos/1")
    assert respuesta.status == 204



def test_crear_producto_datos_invalidos(api_autenticada):
    datos = {"nombre": "X", "precio": -10.0, "stock": -1}
    respuesta = api_autenticada.post("/api/productos", data=datos)
    assert respuesta.status == 400
    cuerpo = respuesta.json()
    assert "errores" in cuerpo


def test_obtener_producto_inexistente_responde_404(api_autenticada):
    respuesta = api_autenticada.get("/api/productos/999")
    assert respuesta.status == 404


def test_actualizar_producto_inexistente_responde_404(api_autenticada):
    datos = {"nombre": "Inexistente", "precio": 100.0, "stock": 10}
    respuesta = api_autenticada.put("/api/productos/999", data=datos)
    assert respuesta.status == 404


def test_actualizar_producto_datos_invalidos(api_autenticada):
    datos = {"nombre": "Ab", "precio": -1.0, "stock": 0}
    respuesta = api_autenticada.put("/api/productos/1", data=datos)
    assert respuesta.status == 400
    cuerpo = respuesta.json()
    assert "errores" in cuerpo


def test_eliminar_producto_inexistente_responde_404(api_autenticada):
    respuesta = api_autenticada.delete("/api/productos/999")
    assert respuesta.status == 404
