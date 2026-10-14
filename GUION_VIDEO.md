# Guion para el video (5–7 minutos)

## 1. Presentación (30 s)
"Hola, soy Andrés Méndez. En este video explico la resolución del ejercicio MiniCore de comisiones de semestres pasados, implementado con el patrón MVC en Python con FastAPI y desplegado en Render."

## 2. El problema (45 s)
- Hay vendedores, cada uno con ventas en distintas fechas.
- Se elige un rango de fechas, se suman las ventas de cada vendedor en ese rango y según el total se aplica un porcentaje de comisión.
- Mostrar la tabla de reglas: 15%, 10%, 8%, 6% y 0%.

## 3. Estructura MVC (2 min) — en VS Code
- Abrir la carpeta `app` y señalar las tres carpetas: `models`, `views`, `controllers`.
- **Modelo** → `models/entidades.py`: las tres tablas (Vendedor, Venta, ReglaComision). Explicar que las reglas están en la base y no quemadas en el código.
- **Modelo** → `models/comision.py`: la consulta suma las ventas por vendedor con un `outerjoin` (así salen también los que vendieron $0), y `porcentaje_para` recorre las reglas de mayor a menor y toma la primera que cumple.
- **Controlador** → `controllers/comision_controller.py`: recibe `desde` y `hasta`, valida que existan y que el inicio no sea mayor al fin, llama al modelo y le pasa el resultado a `index.html`. Mencionar que también hay una ruta `/api/comisiones` que devuelve JSON.
- **Vista** → `views/index.html`: solo pinta la tabla con lo que recibe, no calcula nada.
- `seed.py` carga los datos de prueba al arrancar.

## 4. Demo en la nube (1 min 30 s) — abrir el link de Render
- Rango 01/06/2025 – 30/06/2025 → Juan $80, Carlos $0, Mateo $90, Ana $48.
- Explicar uno: Juan vendió 300 + 500 = 800 → 10% → $80.
- Rango 01/05/2025 – 30/06/2025 → Juan sube a $1200 y pasa al 15% ($180).
- Probar fechas al revés para mostrar el mensaje de error.
- Abrir `/ventas` para mostrar los datos y `/docs` para la API.

## 5. Despliegue (45 s)
- Mostrar el repositorio en GitHub.
- Mostrar en Render el servicio: build `pip install -r requirements.txt` y start `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.

## 6. Cierre (15 s)
"Con esto queda separado lo que es datos y lógica (modelo), lo que se muestra (vista) y quién coordina (controlador). Gracias."
