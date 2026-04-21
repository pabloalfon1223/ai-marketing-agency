"""
Google Sheets Synchronization Service for Polt Mobilier

Syncronizes data between Google Sheets and SQLite database:
- POTENCIALES sheet → Potencial model
- PRODUCCION sheet → Produccion model

Workflow:
- Every 10 minutes: sync Sheets → SQLite
- Auto-create Produccion when Potencial reaches QUOTE_ACCEPTED
- Sync updates back to Sheets
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.potencial import Potencial
from app.models.produccion import Produccion
from app.services.google_auth import GoogleAuthService
from datetime import datetime, timezone
import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class SheetsSyncService:
    """Service for syncing Google Sheets with SQLite database"""

    def __init__(self, sheet_id: str, db: AsyncSession):
        """
        Initialize sync service

        Args:
            sheet_id: Google Sheet ID
            db: AsyncSession for database operations
        """
        self.sheet_id = sheet_id
        self.db = db
        self.auth_service = GoogleAuthService

    async def sync_potenciales(self) -> Dict:
        """
        Synchronize POTENCIALES sheet → SQLite

        Steps:
        1. Fetch data from Sheets POTENCIALES tab
        2. For each row:
           - If new: create Potencial in DB
           - If exists: update fields
           - If estado=QUOTE_ACCEPTED: trigger conversion to Produccion
        3. Sync DB changes back to Sheets

        Returns:
            Dict with sync stats (created, updated, converted)
        """
        stats = {"created": 0, "updated": 0, "converted": 0, "error": None}

        try:
            # Get gspread worksheet
            worksheet = self.auth_service.get_worksheet(
                self.sheet_id, "POTENCIALES"
            )
            if not worksheet:
                logger.warning(
                    "Could not access POTENCIALES sheet - Google Auth may not be configured"
                )
                return stats

            # Get all records from sheet
            rows = worksheet.get_all_records()
            logger.info(f"Fetched {len(rows)} rows from POTENCIALES sheet")

            for row in rows:
                try:
                    # Normalize row keys (remove leading/trailing spaces)
                    row = {k.strip(): v for k, v in row.items()}

                    # Skip empty rows
                    if not row.get("NOMBRE"):
                        continue

                    # Check if potencial already exists
                    stmt = select(Potencial).where(
                        Potencial.nombre == row["NOMBRE"]
                    )
                    result = await self.db.execute(stmt)
                    potencial = result.scalar_one_or_none()

                    # Parse date fields
                    fecha_contacto = None
                    if row.get("FECHA_CONTACTO"):
                        try:
                            fecha_contacto = datetime.fromisoformat(
                                row["FECHA_CONTACTO"]
                            )
                        except (ValueError, TypeError):
                            fecha_contacto = datetime.now(timezone.utc)

                    fecha_seguimiento = None
                    if row.get("FECHA_SEGUIMIENTO"):
                        try:
                            fecha_seguimiento = datetime.fromisoformat(
                                row["FECHA_SEGUIMIENTO"]
                            )
                        except (ValueError, TypeError):
                            pass

                    # Parse numeric fields
                    valor_estimado = 0
                    try:
                        valor_estimado = float(row.get("VALOR_ESTIMADO", 0))
                    except (ValueError, TypeError):
                        valor_estimado = 0

                    if not potencial:
                        # Create new potencial
                        potencial = Potencial(
                            nombre=row.get("NOMBRE", ""),
                            mueble=row.get("MUEBLE", ""),
                            fecha_contacto=fecha_contacto or datetime.now(
                                timezone.utc
                            ),
                            estado=row.get("ESTADO", "SIN_RESPUESTA"),
                            quien_lo_tiene=row.get("QUIEN_LO_TIENE", ""),
                            telefono=row.get("TELEFONO", ""),
                            nota=row.get("NOTA", ""),
                            fecha_seguimiento=fecha_seguimiento,
                            valor_estimado=valor_estimado,
                            sincronizado_sheets=True,
                        )
                        self.db.add(potencial)
                        stats["created"] += 1
                        logger.info(f"Created potencial: {potencial.nombre}")
                    else:
                        # Update existing potencial
                        potencial.mueble = row.get("MUEBLE", potencial.mueble)
                        potencial.fecha_contacto = (
                            fecha_contacto or potencial.fecha_contacto
                        )
                        potencial.estado = row.get("ESTADO", potencial.estado)
                        potencial.quien_lo_tiene = row.get(
                            "QUIEN_LO_TIENE", potencial.quien_lo_tiene
                        )
                        potencial.telefono = row.get(
                            "TELEFONO", potencial.telefono
                        )
                        potencial.nota = row.get("NOTA", potencial.nota)
                        potencial.fecha_seguimiento = (
                            fecha_seguimiento or potencial.fecha_seguimiento
                        )
                        potencial.valor_estimado = valor_estimado
                        potencial.updated_at = datetime.now(timezone.utc)
                        potencial.sincronizado_sheets = True
                        stats["updated"] += 1
                        logger.info(f"Updated potencial: {potencial.nombre}")

                    # Check for conversion to PRODUCCION
                    if potencial.estado == "QUOTE_ACCEPTED":
                        if not potencial.orden_id_asignada:
                            produccion = (
                                await self.convert_potencial_to_produccion(
                                    potencial
                                )
                            )
                            if produccion:
                                stats["converted"] += 1
                                logger.info(
                                    f"Converted {potencial.nombre} to produccion"
                                )

                except Exception as row_error:
                    logger.error(
                        f"Error processing row {row.get('NOMBRE', 'Unknown')}: {str(row_error)}"
                    )
                    continue

            await self.db.commit()
            logger.info(f"Potenciales sync completed: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error syncing potenciales: {str(e)}")
            stats["error"] = str(e)
            await self.db.rollback()
            return stats

    async def sync_produccion(self) -> Dict:
        """
        Synchronize PRODUCCION sheet → SQLite

        Steps:
        1. Fetch data from Sheets PRODUCCION tab
        2. For each row:
           - If new: create Produccion in DB
           - If exists: update (estado, fechas, costo, notas)
        3. Sync DB changes back to Sheets

        Returns:
            Dict with sync stats (created, updated)
        """
        stats = {"created": 0, "updated": 0, "error": None}

        try:
            # Get gspread worksheet
            worksheet = self.auth_service.get_worksheet(
                self.sheet_id, "PRODUCCION"
            )
            if not worksheet:
                logger.warning(
                    "Could not access PRODUCCION sheet - Google Auth may not be configured"
                )
                return stats

            # Get all records from sheet
            rows = worksheet.get_all_records()
            logger.info(f"Fetched {len(rows)} rows from PRODUCCION sheet")

            for row in rows:
                try:
                    # Normalize row keys (remove leading/trailing spaces)
                    row = {k.strip(): v for k, v in row.items()}

                    # Skip empty rows
                    if not row.get("ORDEN_ID"):
                        continue

                    # Check if produccion already exists
                    stmt = select(Produccion).where(
                        Produccion.orden_id == row["ORDEN_ID"]
                    )
                    result = await self.db.execute(stmt)
                    produccion = result.scalar_one_or_none()

                    # Parse date fields
                    fecha_inicio = None
                    if row.get("FECHA_INICIO"):
                        try:
                            fecha_inicio = datetime.fromisoformat(
                                row["FECHA_INICIO"]
                            )
                        except (ValueError, TypeError):
                            fecha_inicio = datetime.now(timezone.utc)

                    fecha_entrega_est = None
                    if row.get("FECHA_ENTREGA_EST"):
                        try:
                            fecha_entrega_est = datetime.fromisoformat(
                                row["FECHA_ENTREGA_EST"]
                            )
                        except (ValueError, TypeError):
                            pass

                    # Parse numeric fields
                    costo_real = 0
                    try:
                        costo_real = float(row.get("COSTO_REAL", 0))
                    except (ValueError, TypeError):
                        costo_real = 0

                    precio_final = 0
                    try:
                        precio_final = float(row.get("PRECIO_FINAL", 0))
                    except (ValueError, TypeError):
                        precio_final = 0

                    if not produccion:
                        # Create new produccion order
                        produccion = Produccion(
                            orden_id=row.get("ORDEN_ID", ""),
                            cliente=row.get("CLIENTE", ""),
                            mueble=row.get("MUEBLE", ""),
                            estado=row.get("ESTADO", "ACCEPTED"),
                            fecha_inicio=fecha_inicio or datetime.now(
                                timezone.utc
                            ),
                            fecha_entrega_est=fecha_entrega_est,
                            productor=row.get("PRODUCTOR", ""),
                            costo_real=costo_real,
                            precio_final=precio_final,
                            notas=row.get("NOTAS_PRODUCCION", ""),
                            sincronizado_sheets=True,
                        )
                        self.db.add(produccion)
                        stats["created"] += 1
                        logger.info(f"Created produccion: {produccion.orden_id}")
                    else:
                        # Update existing produccion
                        produccion.estado = row.get("ESTADO", produccion.estado)
                        produccion.fecha_inicio = (
                            fecha_inicio or produccion.fecha_inicio
                        )
                        produccion.fecha_entrega_est = (
                            fecha_entrega_est or produccion.fecha_entrega_est
                        )
                        produccion.productor = row.get(
                            "PRODUCTOR", produccion.productor
                        )
                        produccion.costo_real = costo_real
                        produccion.precio_final = precio_final
                        produccion.notas = row.get(
                            "NOTAS_PRODUCCION", produccion.notas
                        )
                        produccion.updated_at = datetime.now(timezone.utc)
                        produccion.sincronizado_sheets = True
                        stats["updated"] += 1
                        logger.info(f"Updated produccion: {produccion.orden_id}")

                except Exception as row_error:
                    logger.error(
                        f"Error processing row {row.get('ORDEN_ID', 'Unknown')}: {str(row_error)}"
                    )
                    continue

            await self.db.commit()
            logger.info(f"Produccion sync completed: {stats}")
            return stats

        except Exception as e:
            logger.error(f"Error syncing produccion: {str(e)}")
            stats["error"] = str(e)
            await self.db.rollback()
            return stats

    async def convert_potencial_to_produccion(self, potencial: Potencial) -> Optional[Produccion]:
        """
        Convert POTENCIAL → PRODUCCION when status reaches QUOTE_ACCEPTED

        Steps:
        1. Get Potencial
        2. Create Produccion with data from Potencial
        3. Assign unique orden_id (ORD-XXX-2026)
        4. Write to Sheets PRODUCCION
        5. Update Potencial.orden_id_asignada

        Args:
            potencial: Potencial instance to convert

        Returns:
            Created Produccion instance or None if error
        """
        try:
            # Generate unique orden_id
            # This would typically query the DB for the next ID
            orden_id = f"ORD-{potencial.id:03d}-2026"

            # Create Produccion
            produccion = Produccion(
                orden_id=orden_id,
                cliente=potencial.nombre,
                mueble=potencial.mueble,
                estado="ACCEPTED",
                fecha_inicio=datetime.now(timezone.utc),
                productor=potencial.quien_lo_tiene,
                potencial_id=potencial.id,
                precio_final=potencial.valor_estimado
            )

            self.db.add(produccion)

            # Update potencial with assigned orden_id
            potencial.orden_id_asignada = orden_id
            potencial.updated_at = datetime.now(timezone.utc)

            await self.db.commit()
            await self.db.refresh(produccion)

            logger.info(f"Converted potencial {potencial.id} to produccion {orden_id}")
            return produccion

        except Exception as e:
            logger.error(f"Error converting potencial: {str(e)}")
            await self.db.rollback()
            return None
