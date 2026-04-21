# Polt Mobilier - Integración Google Sheets + Sistema de Dashboards

## 📊 Sistema Completo Implementado

### ✅ Fase 2: Backend (Completado)

#### Base de Datos (SQLAlchemy)
- **Modelo Potencial**: Gestión de clientes potenciales
  - 11 campos: nombre, mueble, fecha_contacto, estado, quien_lo_tiene, telefono, nota, fecha_seguimiento, valor_estimado, orden_id_asignada
  - Estados: SIN_RESPUESTA, ESPERAMOS_RESPUESTA, COTIZACION_ENVIADA, QUOTE_ACCEPTED
  - Timestamps: created_at, updated_at
  - Tracking: sincronizado_sheets

- **Modelo Produccion**: Órdenes de producción
  - 12 campos: orden_id, cliente, mueble, estado, fecha_inicio, fecha_entrega_est, productor, costo_real, precio_final, notas, potencial_id (FK)
  - Estados: ACCEPTED, IN_PRODUCTION, COMPLETED, DELIVERED
  - Timestamps y tracking incluidos

#### API FastAPI (Endpoints)
- **POTENCIALES**
  - `GET /api/v1/potenciales` - Listar (con filtro por estado)
  - `GET /api/v1/potenciales/{id}` - Obtener por ID
  - `POST /api/v1/potenciales` - Crear nuevo
  - `PUT /api/v1/potenciales/{id}` - Actualizar
  - `POST /api/v1/potenciales/{id}/convert` - Convertir a QUOTE_ACCEPTED

- **PRODUCCION**
  - `GET /api/v1/produccion` - Listar (con filtro por estado)
  - `GET /api/v1/produccion/{orden_id}` - Obtener por orden_id
  - `POST /api/v1/produccion` - Crear nueva orden
  - `PUT /api/v1/produccion/{orden_id}` - Actualizar orden

- **DASHBOARDS** (Gráficos y Métricas)
  - `GET /api/v1/dashboards/potenciales/funnel` - Funnel data (count por estado)
  - `GET /api/v1/dashboards/potenciales/value-by-status` - Valor estimado agrupado
  - `GET /api/v1/dashboards/potenciales/conversion-rate` - Tasa de conversión
  - `GET /api/v1/dashboards/produccion/timeline` - Timeline para Gantt chart
  - `GET /api/v1/dashboards/produccion/ingresos` - Ingresos totales
  - `GET /api/v1/dashboards/summary` - Resumen consolidado de KPIs

#### Servicios
- **GoogleAuthService** (`app/services/google_auth.py`)
  - Manejo de credenciales OAuth2
  - Inicialización de cliente gspread
  - Métodos helper para abrir sheets y worksheets
  - Soporte para credenciales en archivo o JSON string

- **SheetsSyncService** (`app/services/sheets_sync.py`)
  - Sincronización POTENCIALES: Sheets → SQLite
  - Sincronización PRODUCCION: Sheets → SQLite
  - Conversión automática: POTENCIAL → PRODUCCION cuando estado = QUOTE_ACCEPTED
  - Manejo de errores y rollback en caso de fallos
  - Logging detallado de cada operación

#### Task Scheduling (APScheduler)
- Sincronización automática cada 10 minutos
- Dos jobs: sync_potenciales y sync_produccion
- Integrado en lifespan context manager

### ✅ Fase 3: Frontend (Completado)

#### API Clients (TypeScript)
- **potenciales.ts**: Interfaz Potencial + métodos CRUD
- **produccion.ts**: Interfaz Produccion + métodos CRUD
- **dashboards.ts**: Interfaces para todos los endpoints de dashboards

#### Páginas React (TSX)
1. **Potenciales.tsx**
   - Tabla con columnas: Nombre, Mueble, Estado, Contacto, Valor, Vendedor
   - Filtros: búsqueda por nombre, filtro por estado
   - Tarjetas de estadísticas: Total, Conversion Rate, Valor Total, En Cotización
   - Gráfico Funnel (barras) con porcentajes
   - Botón "Convertir a Producción" en potenciales COTIZACION_ENVIADA
   - Auto-refresh cada 30 segundos

2. **Produccion.tsx**
   - Tabla con columnas: Orden ID, Cliente, Mueble, Estado, Inicio, Entrega Est., Días, Precio, Productor
   - Filtros: búsqueda por cliente, filtro por estado
   - Tarjetas de estadísticas: Total Órdenes, En Producción, Ingresos, Promedio Días
   - Desglose por estado en tarjetas
   - Auto-refresh cada 30 segundos

3. **Dashboards.tsx**
   - **KPIs Principales**: Total Potenciales, Conversion Rate, Valor Estimado, Ingresos Realizados
   - **Gráfico Funnel**: Potenciales por estado (bar chart)
   - **Gráfico Valor**: Distribución de valor estimado por estado
   - **Timeline**: Próximas 10 entregas con duración en días
   - **Resumen Operacional**: Métricas consolidadas
   - **Análisis de Desempeño**: ROI estimado, potenciales sin respuesta, en cotización, aceptadas

#### Componentes UI
- Uso de shadcn/ui components:
  - Table, Card, Badge, Button, Input, Select
  - Recharts para visualización de datos (Bar, Line, Pie, Area charts)
  - Lucide React para iconos

#### Integración en Navegación
- Añadidas 3 nuevas rutas en Sidebar:
  - `/potenciales` - Target icon
  - `/produccion` - Package icon
  - `/dashboards` - TrendingUp icon
- Separadas con dividers en la navegación

### 📦 Dependencias Agregadas

**Backend** (requirements.txt):
```
apscheduler>=3.10.0
gspread>=6.0.0
google-auth-oauthlib>=1.2.0
google-auth-httplib2>=0.2.0
google-api-python-client>=2.100.0
```

**Frontend**: Usa dependencias existentes (recharts, shadcn/ui, etc.)

---

## 🚀 Guía de Instalación y Configuración

### Paso 1: Configurar Google Sheets

1. Seguir la guía completa en `backend/GOOGLE_SHEETS_SETUP.md`
2. Crear dos pestañas en Google Sheets:
   - **POTENCIALES** - con columnas especificadas
   - **PRODUCCION** - con columnas especificadas
3. Guardar el archivo JSON de credenciales en `backend/credentials/google-credentials.json`

### Paso 2: Configurar Backend

```bash
cd backend

# Copiar template de .env
cp .env.example .env

# Actualizar .env con:
# - GOOGLE_SHEETS_ID=tu-sheet-id
# - GOOGLE_CREDENTIALS_PATH=./credentials/google-credentials.json
# - Otras variables necesarias

# Instalar dependencias
pip install -r requirements.txt

# Crear base de datos
python -c "from app.database import create_tables; import asyncio; asyncio.run(create_tables())"

# Ejecutar servidor
uvicorn app.main:app --reload
```

### Paso 3: Probar Google Sheets Integration

```bash
cd backend

# Ejecutar script de prueba
python test_google_sheets.py
```

Debe mostrar:
- ✅ Google Sheets client initialized successfully
- ✅ Sheet opened successfully
- ✅ POTENCIALES sync successful
- ✅ PRODUCCION sync successful

### Paso 4: Configurar Frontend

```bash
cd frontend

# Actualizar .env (si es necesario)
# VITE_API_URL=http://localhost:8000/api/v1

# Instalar dependencias
npm install

# Ejecutar en desarrollo
npm run dev
```

### Paso 5: Verificación End-to-End

1. **Backend en ejecución:**
   ```bash
   # Terminal 1
   cd backend
   uvicorn app.main:app --reload
   ```
   - Verificar: `http://localhost:8000/api/v1/health` → `{"status": "ok"}`
   - Verificar logs: APScheduler should start after 10 seconds

2. **Frontend en ejecución:**
   ```bash
   # Terminal 2
   cd frontend
   npm run dev
   ```
   - Abrir: `http://localhost:5173`

3. **Probar flujo completo:**
   - Agregar fila a Google Sheets POTENCIALES
   - Esperar máx 10 minutos (o ejecutar sync manual)
   - Ver datos en `/potenciales` en la app
   - Cambiar estado a QUOTE_ACCEPTED en Sheets
   - Próxima sincronización debe crear orden en PRODUCCION
   - Ver en `/produccion` y `/dashboards`

---

## 📊 Flujo de Datos Completo

```
Google Sheets (Manual Input)
    ↓ gspread API (cada 10 min)
Sync Worker (Python)
    ↓
SQLite Database
    ↓ FastAPI REST
React Dashboard
    ↓ User Updates
SQLite → Sheets (sync inversa opcional)
```

### Workflow Automático: Conversión POTENCIAL → PRODUCCION

```
1. Usuario en Sheets: POTENCIAL estado = "COTIZACION_ENVIADA"
2. Usuario o sistema: cambia a "QUOTE_ACCEPTED"
3. Worker detecta en próxima sincronización (cada 10 min)
4. Automáticamente:
   - Crea registro en tabla PRODUCCION
   - Asigna orden_id único (ORD-001-2026)
   - Actualiza potencial.orden_id_asignada
   - Escribe cambios en Sheets
5. Dashboard muestra:
   - Potencial marcado como "Convertido"
   - Nueva orden en PRODUCCION
   - Gráficos actualizados
```

---

## 🔍 Monitoreo y Debugging

### Logs del Servidor

```bash
# Ver logs en tiempo real (durante desarrollo)
# En la terminal donde corre uvicorn

# Buscar errores de sincronización
grep "Error syncing" logs/app.log
```

### Endpoints para Debugging

```bash
# Ver potenciales en DB
curl http://localhost:8000/api/v1/potenciales

# Ver órdenes en DB
curl http://localhost:8000/api/v1/produccion

# Ver estadísticas
curl http://localhost:8000/api/v1/dashboards/summary

# Filtrar por estado
curl http://localhost:8000/api/v1/potenciales?estado=QUOTE_ACCEPTED
```

### Problemas Comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| "Cannot connect to API" | Backend no está corriendo | `uvicorn app.main:app --reload` en terminal |
| "Google credentials not found" | Ruta incorrecta o archivo no existe | Verificar `GOOGLE_CREDENTIALS_PATH` en .env |
| "Permission denied" | Sheet no compartida con service account | Compartir sheet con email del service account |
| "No sync happening" | APScheduler no inició | Esperar 10 segundos después de inicio, verificar logs |
| "Tabla vacía en React" | Sin datos en BD | Agregar fila a Google Sheets y esperar sync |

---

## 📈 Próximas Mejoras (Futuro)

- [ ] Sync inversa: cambios en React → Google Sheets
- [ ] WebSocket para updates en tiempo real (sin esperar 10 min)
- [ ] Validaciones en frontend (formularios para crear/editar)
- [ ] Exportar a PDF/Excel desde dashboards
- [ ] Gráficos más avanzados (Gantt chart interactivo para timeline)
- [ ] Filtros de fecha/rango en dashboards
- [ ] Notificaciones cuando potencial llega a QUOTE_ACCEPTED
- [ ] Campos personalizables en Sheets
- [ ] Multi-tenancy para múltiples usuarios/departamentos

---

## 📝 Estructura de Archivos Finales

```
backend/
├── app/
│   ├── api/
│   │   ├── potenciales.py ✅
│   │   ├── produccion.py ✅
│   │   ├── dashboards.py ✅
│   │   └── ... (otros)
│   ├── models/
│   │   ├── potencial.py ✅
│   │   ├── produccion.py ✅
│   │   └── ... (otros)
│   ├── services/
│   │   ├── google_auth.py ✅
│   │   ├── sheets_sync.py ✅
│   │   └── ... (otros)
│   ├── schemas/
│   │   ├── potencial.py ✅
│   │   ├── produccion.py ✅
│   │   └── ... (otros)
│   ├── main.py ✅ (actualizado)
│   ├── config.py ✅ (actualizado)
│   └── database.py (sin cambios)
├── requirements.txt ✅ (actualizado)
├── .env.example ✅ (nuevo)
├── GOOGLE_SHEETS_SETUP.md ✅ (nuevo)
├── test_google_sheets.py ✅ (nuevo)
└── credentials/ (crear y agregar .gitignore)

frontend/
├── src/
│   ├── pages/
│   │   ├── Potenciales.tsx ✅
│   │   ├── Produccion.tsx ✅
│   │   ├── Dashboards.tsx ✅
│   │   └── ... (otros)
│   ├── api/
│   │   ├── potenciales.ts ✅
│   │   ├── produccion.ts ✅
│   │   ├── dashboards.ts ✅
│   │   └── ... (otros)
│   ├── components/
│   │   └── layout/
│   │       └── Sidebar.tsx ✅ (actualizado)
│   └── App.tsx ✅ (actualizado)
```

---

## ✨ Resumen de Cambios

### Backend
- 2 nuevos modelos SQLAlchemy
- 2 nuevos esquemas Pydantic
- 3 nuevos routers FastAPI (potenciales, produccion, dashboards)
- 2 nuevos servicios (google_auth, sheets_sync)
- main.py actualizado con APScheduler
- config.py actualizado con Google Sheets config

### Frontend
- 3 nuevas páginas React (Potenciales, Produccion, Dashboards)
- 3 nuevos API clients (potenciales, produccion, dashboards)
- Sidebar actualizado con nuevas navegaciones
- App.tsx actualizado con nuevas rutas
- Uso de recharts para gráficos
- Uso de shadcn/ui components

### Dependencias
- Backend: +5 librerías (gspread, google-auth-*)
- Frontend: Sin cambios (usa existentes)

---

## 🎯 KPIs Disponibles en Dashboard

1. **Total Potenciales** - Cantidad de clientes en pipeline
2. **Conversion Rate** - % de potenciales que se convirtieron a órdenes
3. **Valor Total Estimado** - Suma de valores estimados de todos los potenciales
4. **Ingresos Realizados** - Suma de precios finales de órdenes completadas/entregadas
5. **Promedio de Días en Producción** - Tiempo promedio entre inicio y entrega
6. **Órdenes Activas** - Cantidad en estado IN_PRODUCTION
7. **ROI Estimado** - (Ingresos - Valor Estimado) / Valor Estimado * 100

---

## 📞 Soporte

Para más información:
- Documentación Google Sheets: `backend/GOOGLE_SHEETS_SETUP.md`
- Test script: `python backend/test_google_sheets.py`
- API docs: `http://localhost:8000/docs` (Swagger UI)

¡Sistema listo para usar! 🚀
