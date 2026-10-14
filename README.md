# MiniCore – Cálculo de Comisiones (MVC con FastAPI)

Aplicación web que calcula la comisión de cada vendedor según el total que vendió dentro de un rango de fechas. Está hecha con el patrón **Modelo – Vista – Controlador**.

- **Deploy:** _https://minicore-comisiones-h2k0.onrender.com_
- **Video:** _https://youtu.be/RUH2DJIUZss_

## Tecnologías

- Python 3.12 + FastAPI
- SQLAlchemy + SQLite (los datos de prueba se cargan solos al iniciar)
- Jinja2 para las vistas HTML
- Render para el despliegue

## Estructura MVC

```
minicore-comisiones/
├── app/
│   ├── main.py                     # arranca FastAPI, carga datos y registra rutas
│   ├── database.py                 # conexión a la base de datos
│   ├── seed.py                     # datos de prueba (vendedores, ventas, reglas)
│   ├── models/                     # MODELO
│   │   ├── entidades.py            # tablas: Vendedor, Venta, ReglaComision
│   │   └── comision.py             # lógica del cálculo de comisiones
│   ├── controllers/                # CONTROLADOR
│   │   └── comision_controller.py  # recibe las peticiones y decide qué vista mostrar
│   ├── views/                      # VISTA
│   │   ├── base.html
│   │   ├── index.html              # formulario de fechas y tabla de resultados
│   │   └── ventas.html             # listado de ventas
│   └── static/estilos.css
├── requirements.txt
└── render.yaml
```

| Capa | Qué hace aquí |
|------|---------------|
| Modelo | Define las tablas y hace el cálculo: suma las ventas de cada vendedor en el rango y busca qué porcentaje le corresponde. |
| Vista | Plantillas HTML que solo muestran los datos que reciben. |
| Controlador | Lee las fechas del formulario, valida, llama al modelo y le pasa el resultado a la vista. |

## Reglas de comisión

| Ventas en el período | Comisión |
|----------------------|----------|
| $1000 o más | 15% |
| $800 – $999 | 10% |
| $600 – $799 | 8% |
| $400 – $599 | 6% |
| Menos de $400 | 0% |

Las reglas están guardadas en la tabla `reglas_comision`, así que se pueden cambiar sin tocar el código.

## Rutas

| Ruta | Descripción |
|------|-------------|
| `GET /` | Página principal con el formulario |
| `GET /?desde=2025-06-01&hasta=2025-06-30` | Calcula y muestra la tabla |
| `GET /ventas` | Lista de todas las ventas registradas |
| `GET /api/comisiones?desde=...&hasta=...` | Mismo cálculo en JSON |
| `GET /docs` | Documentación automática de FastAPI |

## Ejecutar en local

```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux / Mac
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Abrir http://127.0.0.1:8000

## Casos de prueba

| Rango | Juan | Carlos | Mateo | Ana |
|-------|------|--------|-------|-----|
| 01/06/2025 – 30/06/2025 | $80 | $0 | $90 | $48 |
| 01/05/2025 – 30/06/2025 | $180 | $80 | $90 | $48 |
| 10/06/2025 – 25/06/2025 | $30 | $0 | $90 | $0 |

## Despliegue en Render

1. Subir el proyecto a GitHub.
2. En Render: **New → Web Service** y conectar el repositorio.
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Plan Free → **Create Web Service**.

(También se puede usar **New → Blueprint**, que lee el `render.yaml` directamente.)
