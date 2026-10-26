"""NIVEL UNITARIO (componente) — pytest puro.

Objeto de prueba: app/validaciones.py (funciones puras, sin servidor ni navegador).
Técnicas sugeridas: partición de equivalencia y análisis de valores límite.

Ejecuta solo este nivel:   pytest tests/unitarias -v
"""
import pytest

from app.validaciones import validar_credenciales, validar_producto


# ---------------------------------------------------------------- EJEMPLO
def test_credenciales_con_formato_valido_no_tienen_errores():
    assert validar_credenciales("admin", "Admin123") == []


# ---------------------------------------------------------------- PRUEBAS UNITARIAS


@pytest.mark.parametrize("usuario, password, valido", [
    ("", "Admin123", False),            
    ("   ", "Admin123", False),         
    ("admin", "12345", False),         
    ("admin", "123456", True),          
    ("usuario_valido", "pass123", True) 
])
def test_validar_credenciales_casos(usuario, password, valido):
    errores = validar_credenciales(usuario, password)
    assert (errores == []) == valido



def test_producto_con_datos_validos_no_tiene_errores():
    assert validar_producto("Teclado Mecánico", 250.0, 10) == []



@pytest.mark.parametrize("nombre, valido", [
    ("ab", False),                      
    ("abc", True),                     
    ("  abc  ", True),                  
    ("  ab  ", False),                  
    ("a" * 50, True),                   
    ("a" * 51, False),                  
])
def test_limites_nombre_producto(nombre, valido):
    errores = validar_producto(nombre, 100.0, 5)
    assert (errores == []) == valido



@pytest.mark.parametrize("precio, valido", [
    (-0.01, False),                     
    (0, False),                         
    (0.01, True),                       
    (100_000.0, True),                  
    (100_000.01, False),                
])
def test_limites_precio_producto(precio, valido):
    errores = validar_producto("Mouse Gamer", precio, 5)
    assert (errores == []) == valido



@pytest.mark.parametrize("stock, valido", [
    (-1, False),                        
    (0, True),                         
    (1, True),                          
    (1.5, False),                      
    (True, False),                      
])
def test_limites_stock_producto(stock, valido):
    errores = validar_producto("Mouse Gamer", 50.0, stock)
    assert (errores == []) == valido



@pytest.mark.parametrize("precio", ["100", None, True])
def test_precio_no_numerico_es_invalido(precio):
    assert validar_producto("Mouse Gamer", precio, 5) != []