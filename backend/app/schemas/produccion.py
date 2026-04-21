"""
Esquemas Pydantic para validación de datos de PRODUCCION
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProduccionBase(BaseModel):
    """Datos base de producción"""
    cliente: str = Field(..., min_length=1, max_length=200)
    celular: Optional[str] = None
    descripcion_breve: Optional[str] = None
    estado: str = Field(default="PLANIFICACIÓN")


class ProduccionCreate(ProduccionBase):
    """Esquema para crear un nuevo registro de producción"""
    pass


class ProduccionUpdate(BaseModel):
    """Esquema para actualizar un registro de producción"""
    cliente: Optional[str] = None
    celular: Optional[str] = None
    descripcion_breve: Optional[str] = None
    estado: Optional[str] = None


class ProduccionResponse(ProduccionBase):
    """Esquema de respuesta de producción"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProduccionListResponse(BaseModel):
    """Respuesta para listado de producciones"""
    total: int
    items: list[ProduccionResponse]
