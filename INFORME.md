# Informe · Laboratorio 8 · Pruebas automatizadas

**Equipo:** 
**Integrantes:** Jonathan Garcia - 1045222, Daniel Paz - 1200022

## 1. Defectos encontrados

Un reporte por defecto. Deja la prueba que lo detecta FALLANDO en tu entrega.

| ID | Nivel que lo detectó | Prueba (archivo::función) | Pasos para reproducir | Resultado esperado (según la especificación) | Resultado obtenido |
|---|---|---|---|---|---|
| DEF-01 | Unitarias | tests/unitarias/test_unitarias.py::test_limites_precio_producto | Llamamos a validar_producto mandando precio 0 con stock y nombre validos. | Deberia dar error porque la guia dice que el precio tiene que ser mayor a 0. | No da error y lo toma como valido porque en el codigo pusieron precio < 0 en vez de <= 0. |
| DEF-02 | API | tests/api/test_api.py::test_obtener_producto_inexistente_responde_404 | Hacemos un GET a /api/productos/999 mandando el token en la cabecera. | Deberia responder 404 Not Found porque el producto no existe. | Responde 200 OK con un json vacio {}. |
| DEF-03 | E2E | tests/e2e/test_e2e.py::test_eliminar_producto_especifico_sin_efectos_colaterales | Iniciamos sesion con admin y le damos al boton de eliminar en la fila del segundo producto (Mouse). | Deberia eliminarse el Mouse y quedarse el Teclado en la tabla. | Se borra el Teclado y el Mouse sigue en la tabla porque en el html pusieron el id fijo del primer elemento. |

## 2. Tabla comparativa de niveles

Tiempo: ejecuta `pytest tests/<nivel> -q` y anota el tiempo que reporta pytest.

| Criterio | Unitarias | API | E2E |
|---|---|---|---|
| Número de pruebas | 23 | 18 | 6 |
| Tiempo total de ejecución (s) | 0.36 s | 3.37 s | 11.13 s |
| Tiempo promedio por prueba (s) | 0.016 s | 0.187 s | 1.855 s |
| Defectos detectados (IDs) | DEF-01 | DEF-02 | DEF-03 |
| ¿Qué cambio en la app rompería estas pruebas sin que haya un defecto? | Si cambian los nombres de las funciones o hacen que devuelvan otro formato en vez de una lista de errores. | Si cambian las rutas de la api, nombres de campos en los json o el formato del token. | Si cambian textos de botones, nombres de etiquetas o la estructura de las tablas en el html. |
| Costo de mantenimiento (Alto / Medio / Bajo) y por qué | Bajo, porque son funciones simples en memoria y no dependen de nada externo. | Medio, porque si cambia el contrato de la api hay que actualizar las peticiones. | Alto, porque tardan bastante y cualquier cambio visual en el front las puede botar. |

## 3. Recomendación (máximo media página)

El equipo de Inventario IS1 tiene un pipeline de CI. Recomienda qué pruebas correr:

- en cada commit: solo correr las pruebas unitarias. Nos tomaron apenas 0.36 segundos para las 23 pruebas. Son casi instantaneas, no necesitan levantar servidor ni navegador, y nos avisan rapido si rompimos alguna regla antes de subir cambios.
- en cada pull request: correr unitarias y de api. Juntas tardan menos de 4 segundos. Con esto revisamos que la logica y los endpoints con token sigan respondiendo bien antes de hacer merge a la rama principal.
- antes de liberar a producción: correr toda la suite completa incluyendo las e2e. Tardan como 11 segundos por levantar chromium, pero vale la pena para probar la interfaz real con el usuario y ver que los botones y tablas no tengan clavos visuales ni efectos raros.

Justifica con tus datos de la tabla y con la pirámide de pruebas.
Esto coincide con la piramide de pruebas: la base tiene bastantes pruebas unitarias porque son rapidas y baratas de correr, en medio van las de integracion/api para revisar contratos, y arriba dejamos pocas e2e para los flujos criticos porque son las mas lentas y fragiles de mantener.

Responde además: ¿qué defecto NO habría detectado una suite solo de pruebas E2E, o solo de pruebas unitarias?
Una suite solo de E2E no habria detectado el DEF-02 (el 404 al consultar un id inexistente), porque desde la interfaz grafica el usuario solo hace click a lo que ya existe y nadie va a ir a escribir a mano una ruta de api con id invalido.
Y una suite solo de pruebas unitarias jamas habria detectado el DEF-03 (el boton de eliminar que borra el producto equivocado), porque ese bug estaba metido directo en la plantilla html/jinja con un id fijo. Eso solo se podia notar simulando al usuario en el navegador real.
