"""Lógica de negocio del cálculo de comisiones (parte del Modelo en MVC)."""
from datetime import date

from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from app.models.entidades import ReglaComision, Vendedor, Venta


def obtener_reglas(db: Session):
    return db.query(ReglaComision).order_by(ReglaComision.monto_minimo.desc()).all()


def porcentaje_para(total: float, reglas) -> float:
    # las reglas vienen ordenadas de mayor a menor, se toma la primera que cumpla
    for regla in reglas:
        if total >= regla.monto_minimo:
            return regla.porcentaje
    return 0.0


def calcular_comisiones(db: Session, desde: date, hasta: date):
    reglas = obtener_reglas(db)

    totales = (
        db.query(
            Vendedor.nombre,
            func.coalesce(func.sum(Venta.monto), 0).label("total"),
        )
        .outerjoin(
            Venta,
            and_(Venta.vendedor_id == Vendedor.id, Venta.fecha.between(desde, hasta)),
        )
        .group_by(Vendedor.id, Vendedor.nombre)
        .order_by(Vendedor.nombre)
        .all()
    )

    resultado = []
    for nombre, total in totales:
        total = float(total)
        porcentaje = porcentaje_para(total, reglas)
        resultado.append(
            {
                "vendedor": nombre,
                "total_ventas": round(total, 2),
                "porcentaje": porcentaje,
                "comision": round(total * porcentaje, 2),
            }
        )
    return resultado


def listar_ventas(db: Session):
    return (
        db.query(Venta.fecha, Vendedor.nombre, Venta.monto)
        .join(Vendedor)
        .order_by(Venta.fecha)
        .all()
    )
