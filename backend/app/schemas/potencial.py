"""
Esquemas Pydantic para validación de datos de POTENCIALES
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PotencialBase(BaseModel):
    """Datos base del potencial"""
    nombre: str = Field(..., min_length=1, max_length=200)
    mueble: str = Field(..., min_length=1, max_length=100)
    celular: Optional[str] = None
    quien_lo_tiene: Optional[str] = None
    prioridad: str = Field(default="MEDIA")  # ALTA, MEDIA, BAJA
    estado: Optional[str] = Field(default="SIN_RESPUESTA")
    fecha_seguimiento: Optional[datetime] = None


class PotencialCreate(PotencialBase):
    """Esquema para crear un nuevo potencial"""
    fecha: datetime = Field(default_factory=datetime.utcnow)


class PotencialUpdate(BaseModel):
    """Esquema para actualizar un potencial existente"""
    nombre: Optional[str] = None
    mueble: Optional[str] = None
    celular: Optional[str] = None
    quien_lo_tiene: Optional[str] = None
    prioridad: Optional[str] = None
    estado: Optional[str] = None
    fecha: Optional[datetime] = None
    fecha_seguimiento: Optional[datetime] = None


class PotencialResponse(PotencialBase):
    """Esquema de respuesta de potencial"""
    id: int
    fecha: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PotencialListResponse(BaseModel):
    """Respuesta para listado de potenciales"""
    total: int
    items: list[PotencialResponse]
