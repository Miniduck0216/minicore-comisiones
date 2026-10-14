from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Vendedor(Base):
    __tablename__ = "vendedores"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)

    ventas = relationship("Venta", back_populates="vendedor")


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True)
    vendedor_id = Column(Integer, ForeignKey("vendedores.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)

    vendedor = relationship("Vendedor", back_populates="ventas")


class ReglaComision(Base):
    """Cada fila dice: si el total vendido es >= monto_minimo, se aplica ese porcentaje."""

    __tablename__ = "reglas_comision"

    id = Column(Integer, primary_key=True)
    monto_minimo = Column(Float, nullable=False)
    porcentaje = Column(Float, nullable=False)
