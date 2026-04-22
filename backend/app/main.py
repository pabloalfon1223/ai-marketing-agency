import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.database import create_tables
from app.api import clients, projects, campaigns, content, agents, analytics, websocket, purchases, orders, ideas, checkout
import asyncio
import logging

logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Create data directory for SQLite
        os.makedirs("data", exist_ok=True)
        # Create tables on startup
        await create_tables()
        logger.info("✅ Database tables created/verified")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")

    try:
        # Initialize task queue
        from app.services.task_queue import task_queue
        await task_queue.start()
        logger.info("✅ Task queue initialized")
    except Exception as e:
        logger.warning(f"⚠️ Error initializing task queue: {str(e)}")

    try:
        # Initialize APScheduler for Sheets sync (every 10 minutes)
        from apscheduler.schedulers.asyncio import AsyncIOScheduler
        from app.database import AsyncSessionLocal
        from app.services.sheets_sync import SheetsSyncService

        scheduler = AsyncIOScheduler()

        async def sync_potenciales_task():
            """Background task to sync POTENCIALES every 10 minutes"""
            try:
                async with AsyncSessionLocal() as db:
                    sheet_id = os.getenv("GOOGLE_SHEETS_ID", "")
                    if sheet_id:
                        sync_service = SheetsSyncService(sheet_id, db)
                        result = await sync_service.sync_potenciales()
                        logger.info(f"Potenciales sync: {result}")
            except Exception as e:
                logger.error(f"Error in potenciales sync task: {str(e)}")

        async def sync_produccion_task():
            """Background task to sync PRODUCCION every 10 minutes"""
            try:
                async with AsyncSessionLocal() as db:
                    sheet_id = os.getenv("GOOGLE_SHEETS_ID", "")
                    if sheet_id:
                        sync_service = SheetsSyncService(sheet_id, db)
                        result = await sync_service.sync_produccion()
                        logger.info(f"Produccion sync: {result}")
            except Exception as e:
                logger.error(f"Error in produccion sync task: {str(e)}")

        # Add jobs: sync every 10 minutes
        scheduler.add_job(sync_potenciales_task, "interval", minutes=10, id="sync_potenciales")
        scheduler.add_job(sync_produccion_task, "interval", minutes=10, id="sync_produccion")

        scheduler.start()
        logger.info("✅ APScheduler started: Sheets sync scheduled (si Google Sheets está configurado)")
    except Exception as e:
        logger.warning(f"⚠️ Error initializing APScheduler: {str(e)}")
        scheduler = None

    yield

    # Shutdown
    try:
        await task_queue.stop()
    except:
        pass

    try:
        if scheduler:
            scheduler.shutdown()
        logger.info("✅ APScheduler stopped")
    except:
        pass


app = FastAPI(
    title="AI Marketing Agency",
    description="Sistema de agentes IA para marketing completo",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(content.router, prefix="/api/v1/content", tags=["content"])
app.include_router(agents.router, prefix="/api/v1", tags=["agents"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(purchases.router, prefix="/api/v1", tags=["purchases"])
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
app.include_router(ideas.router, prefix="/api/v1", tags=["ideas"])
app.include_router(checkout.router, prefix="/api/v1", tags=["checkout"])
app.include_router(websocket.router, tags=["websocket"])

# Polt Mobilier routers (con manejo de errores)
try:
    from app.api import potenciales, produccion, dashboards
    app.include_router(potenciales.router)
    app.include_router(produccion.router)
    app.include_router(dashboards.router)
    logger.info("✅ Polt Mobilier routers cargados exitosamente")
except Exception as e:
    logger.warning(f"⚠️ Error cargando routers de Polt Mobilier: {str(e)}")
    logger.info("La app inicia sin Polt Mobilier routers, pero otros endpoints funcionan")


@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok", "service": "AI Marketing Agency"}
