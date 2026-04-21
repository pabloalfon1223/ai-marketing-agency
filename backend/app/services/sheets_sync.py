"""
Servicio de Sincronización con Google Sheets para Polt Mobilier

Sincroniza datos entre Google Sheets y base de datos SQLite:
- Hoja POTENCIALES → Modelo Potencial
- Hoja PRODUCCION → Modelo Produccion

Flujo de trabajo:
- Cada 10 minutos: sincroniza Sheets → SQLite
- Auto-crea PRODUCCION cuando POTENCIAL.estado = "CLIENTE"
- Sincroniza actualizaciones de SQLite → Sheets
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.potencial import Potencial
from app.models.produccion import Produccion
from app.services.google_auth import GoogleAuthService
from app.services.gmail_notifications import notification_service
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

# Estados válidos para PRODUCCION (se mantienen todos los 8)
ESTADOS_PRODUCCION_VALIDOS = [
    "PLANIFICACIÓN",
    "CARPINTERIA",
    "LAQUEADO",
    "RETIRO PARA REMODELAR",
    "PENDIENTE",
    "POST VENTA",
    "FIDELIZACION",
    "FINALIZADO"
]

# Estados válidos para POTENCIALES
ESTADOS_POTENCIAL_VALIDOS = [
    "SIN_RESPUESTA",
    "ESPERAMOS_RESPUESTA",
    "COTIZACION_ENVIADA",
    "CLIENTE",
    "CERRAR",
    "RECONTACTAR"
]

# Prioridades válidas
PRIORIDADES_VALIDAS = ["ALTA", "MEDIA", "BAJA"]


class SheetsSyncService:
    """Servicio para sincronizar Google Sheets con base de datos SQLite"""

    def __init__(self, sheet_id: str, db: AsyncSession):
        """
        Inicializar servicio de sincronización

        Args:
            sheet_id: ID de la hoja de Google Sheets
            db: AsyncSession para operaciones de base de datos
        """
        self.sheet_id = sheet_id
        self.db = db
        self.auth_service = GoogleAuthService

    async def sync_potenciales(self) -> Dict:
        """
        Sincronizar hoja POTENCIALES → SQLite

        Pasos:
        1. Obtener datos de la hoja POTENCIALES en Sheets
        2. Para cada fila:
           - Si es nueva: crear Potencial en BD
           - Si existe: actualizar campos
           - Si estado=CLIENTE: desencadenar conversión a Produccion
        3. Sincronizar cambios de BD de vuelta a Sheets

        Retorna:
            Dict con estadísticas (creados, actualizados, convertidos)
        """
        stats = {"created": 0, "updated": 0, "converted": 0, "error": None}

        try:
            # Obtener worksheet de Google Sheets
            worksheet = self.auth_service.get_worksheet(
                self.sheet_id, "POTENCIALES"
            )
            if not worksheet:
                logger.warning(
                    "No se pudo acceder a la hoja POTENCIALES - Google Auth podría no estar configurado"
                )
                return stats

            # Obtener todos los registros de la hoja
            rows = worksheet.get_all_records()
            logger.info(f"Se obtuvieron {len(rows)} filas de la hoja POTENCIALES")

            for row in rows:
                try:
                    # Normalizar claves de fila (remover espacios iniciales/finales)
                    row = {k.strip(): v for k, v in row.items()}

                    # Saltar filas vacías
                    if not row.get("NOMBRE"):
                        continue

                    # Verificar si el potencial ya existe
                    stmt = select(Potencial).where(
                        Potencial.nombre == row["NOMBRE"]
                    )
                    result = await self.db.execute(stmt)
                    potencial = result.scalar_one_or_none()

                    # Guardar estado anterior para detectar cambios
                    estado_anterior = potencial.estado if potencial else None

                    # Parsear campos de fecha
                    fecha = None
                    if row.get("FECHA"):
                        try:
                            fecha = datetime.fromisoformat(row["FECHA"])
                        except (ValueError, TypeError):
                            fecha = datetime.now(timezone.utc)

                    fecha_seguimiento = None
                    if row.get("FECHA_SEGUIMIENTO"):
                        try:
                            fecha_seguimiento = datetime.fromisoformat(
                                row["FECHA_SEGUIMIENTO"]
                            )
                        except (ValueError, TypeError):
                            pass

                    # Validar prioridad
                    prioridad = row.get("PRIORIDAD", "MEDIA")
                    if prioridad not in PRIORIDADES_VALIDAS:
                        prioridad = "MEDIA"

                    # Validar estado
                    estado = row.get("ESTADO", "SIN_RESPUESTA")
                    if estado not in ESTADOS_POTENCIAL_VALIDOS:
                        estado = "SIN_RESPUESTA"

                    if not potencial:
                        # Crear nuevo potencial
                        potencial = Potencial(
                            nombre=row.get("NOMBRE", ""),
                            mueble=row.get("MUEBLE", ""),
                            fecha=fecha or datetime.now(timezone.utc),
                            estado=estado,
                            quien_lo_tiene=row.get("QUIEN_LO_TIENE", ""),
                            celular=row.get("CELULAR", ""),
                            fecha_seguimiento=fecha_seguimiento,
                            prioridad=prioridad,
                        )
                        self.db.add(potencial)
                        stats["created"] += 1
                        logger.info(f"Potencial creado: {potencial.nombre}")
                    else:
                        # Actualizar potencial existente
                        potencial.mueble = row.get("MUEBLE", potencial.mueble)
                        potencial.fecha = fecha or potencial.fecha
                        potencial.estado = estado
                        potencial.quien_lo_tiene = row.get(
                            "QUIEN_LO_TIENE", potencial.quien_lo_tiene
                        )
                        potencial.celular = row.get("CELULAR", potencial.celular)
                        potencial.fecha_seguimiento = (
                            fecha_seguimiento or potencial.fecha_seguimiento
                        )
                        potencial.prioridad = prioridad
                        potencial.updated_at = datetime.now(timezone.utc)
                        stats["updated"] += 1
                        logger.info(f"Potencial actualizado: {potencial.nombre}")

                    # Verificar si cambió a "CLIENTE" para trigger de conversión
                    if (estado_anterior != "CLIENTE" and estado == "CLIENTE"):
                        # Se detectó cambio a CLIENTE - proceder con conversión
                        produccion = (
                            await self.convertir_potencial_a_produccion(
                                potencial
                            )
                        )
                        if produccion:
                            stats["converted"] += 1
                            logger.info(
                                f"Convertido: {potencial.nombre} → PRODUCCION"
                            )

                except Exception as row_error:
                    logger.error(
                        f"Error procesando fila {row.get('NOMBRE', 'Desconocido')}: {str(row_error)}"
                    )
                    continue

            await self.db.commit()
            logger.info(f"Sincronización de POTENCIALES completada: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error sincronizando POTENCIALES: {str(e)}")
            stats["error"] = str(e)
            await self.db.rollback()
            return stats

    async def sync_produccion(self) -> Dict:
        """
        Sincronizar hoja PRODUCCION → SQLite

        Pasos:
        1. Obtener datos de la hoja PRODUCCION en Sheets
        2. Para cada fila:
           - Si es nueva: crear Produccion en BD
           - Si existe: actualizar (estado, fechas, descripción)
        3. Sincronizar cambios de BD de vuelta a Sheets

        Retorna:
            Dict con estadísticas (creados, actualizados)
        """
        stats = {"created": 0, "updated": 0, "error": None}

        try:
            # Obtener worksheet de Google Sheets
            worksheet = self.auth_service.get_worksheet(
                self.sheet_id, "PRODUCCION"
            )
            if not worksheet:
                logger.warning(
                    "No se pudo acceder a la hoja PRODUCCION - Google Auth podría no estar configurado"
                )
                return stats

            # Obtener todos los registros de la hoja
            rows = worksheet.get_all_records()
            logger.info(f"Se obtuvieron {len(rows)} filas de la hoja PRODUCCION")

            for row in rows:
                try:
                    # Normalizar claves de fila (remover espacios iniciales/finales)
                    row = {k.strip(): v for k, v in row.items()}

                    # Saltar filas vacías
                    if not row.get("CLIENTE"):
                        continue

                    # Verificar si la producción ya existe (por nombre de cliente)
                    stmt = select(Produccion).where(
                        Produccion.cliente == row["CLIENTE"]
                    )
                    result = await self.db.execute(stmt)
                    produccion = result.scalar_one_or_none()

                    # Validar estado - mantener todos los 8 estados
                    estado = row.get("ESTADO", "PLANIFICACIÓN")
                    if estado not in ESTADOS_PRODUCCION_VALIDOS:
                        estado = "PLANIFICACIÓN"

                    # Parsear campos de fecha
                    fecha_creacion = None
                    if row.get("FECHA_CREACION"):
                        try:
                            fecha_creacion = datetime.fromisoformat(
                                row["FECHA_CREACION"]
                            )
                        except (ValueError, TypeError):
                            fecha_creacion = datetime.now(timezone.utc)

                    if not produccion:
                        # Crear nuevo registro de producción
                        produccion = Produccion(
                            cliente=row.get("CLIENTE", ""),
                            celular=row.get("CELULAR", ""),
                            descripcion_breve=row.get("DESCRIPCION_BREVE", ""),
                            estado=estado,
                            created_at=fecha_creacion or datetime.now(timezone.utc),
                        )
                        self.db.add(produccion)
                        stats["created"] += 1
                        logger.info(f"Producción creada: {produccion.cliente}")
                    else:
                        # Actualizar producción existente
                        produccion.celular = row.get("CELULAR", produccion.celular)
                        produccion.descripcion_breve = row.get(
                            "DESCRIPCION_BREVE", produccion.descripcion_breve
                        )
                        produccion.estado = estado
                        produccion.updated_at = datetime.now(timezone.utc)
                        stats["updated"] += 1
                        logger.info(f"Producción actualizada: {produccion.cliente}")

                except Exception as row_error:
                    logger.error(
                        f"Error procesando fila {row.get('CLIENTE', 'Desconocido')}: {str(row_error)}"
                    )
                    continue

            await self.db.commit()
            logger.info(f"Sincronización de PRODUCCION completada: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error sincronizando PRODUCCION: {str(e)}")
            stats["error"] = str(e)
            await self.db.rollback()
            return stats

    async def convertir_potencial_a_produccion(self, potencial: Potencial) -> Optional[Produccion]:
        """
        Convertir POTENCIAL → PRODUCCION cuando el estado llega a "CLIENTE"

        Pasos:
        1. Obtener Potencial
        2. Crear Produccion con datos del Potencial
        3. Estado inicial: PLANIFICACIÓN
        4. Escribir en hoja PRODUCCION de Sheets
        5. Enviar notificación por Gmail

        Args:
            potencial: Instancia de Potencial a convertir

        Retorna:
            Instancia de Produccion creada, o None si hay error
        """
        try:
            # Crear Produccion con datos del Potencial
            produccion = Produccion(
                cliente=potencial.nombre,
                celular=potencial.celular,
                descripcion_breve=potencial.mueble,
                estado="PLANIFICACIÓN",  # Estado inicial al convertir
                created_at=datetime.now(timezone.utc),
            )

            self.db.add(produccion)
            await self.db.flush()  # Obtener el ID de la nueva producción

            # Enviar notificación por Gmail
            await notification_service.notificar_potencial_convertido(
                nombre=potencial.nombre,
                mueble=potencial.mueble,
                celular=potencial.celular
            )

            await self.db.commit()
            await self.db.refresh(produccion)

            logger.info(
                f"Convertido: {potencial.nombre} (ID: {potencial.id}) → PRODUCCION (ID: {produccion.id})"
            )
            return produccion

        except Exception as e:
            logger.error(f"Error al convertir potencial: {str(e)}")
            await self.db.rollback()
            return None
