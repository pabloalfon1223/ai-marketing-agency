from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProduccionBase(BaseModel):
    orden_id: str
    cliente: str
    mueble: str
    estado: str = "ACCEPTED"
    fecha_inicio: datetime
    fecha_entrega_est: Optional[datetime] = None
    productor: Optional[str] = None
    costo_real: Optional[float] = None
    precio_final: Optional[float] = None
    notas: Optional[str] = None
    potencial_id: Optional[int] = None


class ProduccionCreate(ProduccionBase):
    """Schema para crear una nueva orden de producción"""
    pass


class ProduccionUpdate(BaseModel):
    """Schema para actualizar una orden de producción"""
    estado: Optional[str] = None
    fecha_entrega_est: Optional[datetime] = None
    productor: Optional[str] = None
    costo_real: Optional[float] = None
    precio_final: Optional[float] = None
    notas: Optional[str] = None


class ProduccionResponse(ProduccionBase):
    """Schema para respuestas de producción"""
    id: int
    sincronizado_sheets: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
