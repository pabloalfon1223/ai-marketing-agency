from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class PotencialBase(BaseModel):
    nombre: str
    mueble: str
    fecha_contacto: datetime
    estado: str = "SIN_RESPUESTA"
    quien_lo_tiene: Optional[str] = None
    telefono: Optional[str] = None
    nota: Optional[str] = None
    fecha_seguimiento: Optional[datetime] = None
    valor_estimado: Optional[float] = None


class PotencialCreate(PotencialBase):
    """Schema para crear un nuevo potencial"""
    pass


class PotencialUpdate(BaseModel):
    """Schema para actualizar un potencial"""
    nombre: Optional[str] = None
    mueble: Optional[str] = None
    fecha_contacto: Optional[datetime] = None
    estado: Optional[str] = None
    quien_lo_tiene: Optional[str] = None
    telefono: Optional[str] = None
    nota: Optional[str] = None
    fecha_seguimiento: Optional[datetime] = None
    valor_estimado: Optional[float] = None


class PotencialResponse(PotencialBase):
    """Schema para respuestas de potencial"""
    id: int
    orden_id_asignada: Optional[str] = None
    sincronizado_sheets: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
