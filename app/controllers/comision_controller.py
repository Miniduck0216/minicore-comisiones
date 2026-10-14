from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.comision import calcular_comisiones, listar_ventas, obtener_reglas

router = APIRouter()
templates = Jinja2Templates(directory=Path(__file__).resolve().parent.parent / "views")


def _parsear_fecha(valor: str | None):
    if not valor:
        return None
    try:
        return date.fromisoformat(valor)
    except ValueError:
        return None


@router.get("/", response_class=HTMLResponse)
def inicio(
    request: Request,
    desde: str | None = None,
    hasta: str | None = None,
    db: Session = Depends(get_db),
):
    fecha_desde = _parsear_fecha(desde)
    fecha_hasta = _parsear_fecha(hasta)
    resultados = None
    error = None

    if desde is not None or hasta is not None:
        if not fecha_desde or not fecha_hasta:
            error = "Selecciona las dos fechas."
        elif fecha_desde > fecha_hasta:
            error = "La fecha de inicio no puede ser mayor a la fecha final."
        else:
            resultados = calcular_comisiones(db, fecha_desde, fecha_hasta)

    total_comisiones = sum(r["comision"] for r in resultados) if resultados else 0

    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "desde": desde or "",
            "hasta": hasta or "",
            "resultados": resultados,
            "total_comisiones": total_comisiones,
            "error": error,
            "reglas": obtener_reglas(db),
        },
    )


@router.get("/ventas", response_class=HTMLResponse)
def ventas(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse(request, "ventas.html", {"ventas": listar_ventas(db)})


@router.get("/api/comisiones")
def api_comisiones(desde: date, hasta: date, db: Session = Depends(get_db)):
    if desde > hasta:
        raise HTTPException(status_code=400, detail="La fecha de inicio es mayor a la final")
    return {
        "rango": {"desde": desde, "hasta": hasta},
        "resultado": calcular_comisiones(db, desde, hasta),
    }
