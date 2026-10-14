"""Carga los datos de prueba del ejercicio si la base está vacía."""
from datetime import date

from app.database import Base, SessionLocal, engine
from app.models import ReglaComision, Vendedor, Venta


def cargar_datos():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Vendedor).count() > 0:
            return

        juan = Vendedor(nombre="Juan")
        carlos = Vendedor(nombre="Carlos")
        mateo = Vendedor(nombre="Mateo")
        ana = Vendedor(nombre="Ana")
        db.add_all([juan, carlos, mateo, ana])
        db.flush()

        db.add_all(
            [
                Venta(vendedor_id=juan.id, fecha=date(2025, 5, 21), monto=400),
                Venta(vendedor_id=juan.id, fecha=date(2025, 6, 9), monto=300),
                Venta(vendedor_id=juan.id, fecha=date(2025, 6, 24), monto=500),
                Venta(vendedor_id=carlos.id, fecha=date(2025, 5, 29), monto=600),
                Venta(vendedor_id=carlos.id, fecha=date(2025, 6, 3), monto=200),
                Venta(vendedor_id=mateo.id, fecha=date(2025, 6, 11), monto=900),
                Venta(vendedor_id=ana.id, fecha=date(2025, 6, 30), monto=600),
            ]
        )

        db.add_all(
            [
                ReglaComision(monto_minimo=1000, porcentaje=0.15),
                ReglaComision(monto_minimo=800, porcentaje=0.10),
                ReglaComision(monto_minimo=600, porcentaje=0.08),
                ReglaComision(monto_minimo=400, porcentaje=0.06),
            ]
        )
        db.commit()
    finally:
        db.close()
