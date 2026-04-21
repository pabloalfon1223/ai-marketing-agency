# 🚀 Quick Start - Polt Mobilier System

## 5 Minutos para Levantar el Sistema

### 1️⃣ Backend: Instalación (2 min)

```bash
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Crear .env (copiar desde .env.example)
cp .env.example .env

# Mínimo que debe ir en .env:
# GOOGLE_SHEETS_ID=tu-sheet-id-aqui
# GOOGLE_CREDENTIALS_PATH=./credentials/google-credentials.json
```

### 2️⃣ Google Sheets: Configuración (2 min)

**Opción A: Usar sin Google Sheets (solo local)**
- El sistema funciona sin Google Sheets
- Los datos se guardan en SQLite local
- La sincronización simplemente no hará nada
- ✅ Perfecto para probar la UI

**Opción B: Conectar Google Sheets (necesita credenciales)**
1. Ver guía completa: `backend/GOOGLE_SHEETS_SETUP.md`
2. Copiar credenciales JSON a: `backend/credentials/google-credentials.json`
3. Obtener Sheet ID de tu Google Sheet
4. Actualizar `.env` con estos valores

### 3️⃣ Backend: Ejecutar (1 min)

```bash
cd backend
uvicorn app.main:app --reload
```

Debería ver:
```
✓ INFO:     Application startup complete
✓ INFO:     APScheduler started: Sheets sync scheduled for every 10 minutes
```

**Verificar:** `curl http://localhost:8000/api/v1/health`

### 4️⃣ Frontend: Ejecutar

```bash
cd frontend
npm run dev
```

Abrir: `http://localhost:5173`

---

## ✨ Lo que Tienes Funcionando

### Páginas Disponibles (en la barra izquierda):

| Página | Descripción | Ruta |
|--------|-----------|------|
| **Potenciales** | Tabla + estadísticas de clientes potenciales | `/potenciales` |
| **Producción** | Tabla + timeline de órdenes en producción | `/produccion` |
| **Dashboards** | Gráficos consolidados + KPIs | `/dashboards` |

### Endpoints API (para testing):

```bash
# Ver potenciales
curl http://localhost:8000/api/v1/potenciales

# Ver órdenes
curl http://localhost:8000/api/v1/produccion

# Ver estadísticas
curl http://localhost:8000/api/v1/dashboards/summary
```

---

## 🧪 Probar Sin Google Sheets

### Paso 1: Agregar datos de prueba

```bash
# Abrir terminal Python en el directorio backend
python

# Dentro de Python:
import asyncio
from app.database import AsyncSessionLocal
from app.models.potencial import Potencial
from datetime import datetime, timezone

async def add_test_data():
    async with AsyncSessionLocal() as db:
        # Crear potencial de prueba
        p = Potencial(
            nombre="Test Cliente",
            mueble="Biblioteca",
            fecha_contacto=datetime.now(timezone.utc),
            estado="COTIZACION_ENVIADA",
            quien_lo_tiene="Juan",
            telefono="1234567890",
            valor_estimado=50000
        )
        db.add(p)
        await db.commit()
        print("✅ Potencial de prueba creado")

asyncio.run(add_test_data())
```

### Paso 2: Ver en la aplicación

1. Ir a `http://localhost:5173/potenciales`
2. Deberías ver la fila de prueba

### Paso 3: Convertir a Producción

1. Click en "Convertir" en la fila
2. Cambiar estado a "QUOTE_ACCEPTED" manualmente:

```python
# En Python nuevamente:
async def test_convert():
    async with AsyncSessionLocal() as db:
        p = await db.execute(select(Potencial).where(Potencial.nombre == "Test Cliente"))
        potencial = p.scalar_one()
        potencial.estado = "QUOTE_ACCEPTED"
        await db.commit()
        print("✅ Potencial convertido a QUOTE_ACCEPTED")
        
        # Ahora ejecutar sync manualmente
        from app.services.sheets_sync import SheetsSyncService
        sync = SheetsSyncService("fake-id", db)
        result = await sync.convert_potencial_to_produccion(potencial)
        print(f"✅ Orden creada: {result}")

asyncio.run(test_convert())
```

3. Ir a `http://localhost:5173/produccion`
4. ¡Deberías ver la nueva orden!

---

## 🔗 Conectar Google Sheets (Opcional)

### Pasos Rápidos:

1. **Crear Service Account en Google Cloud:**
   - Ir a: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Crear nuevo Service Account
   - Crear JSON key
   - Descargar

2. **Crear Google Sheet:**
   - Ir a: https://sheets.google.com
   - Crear nuevo sheet
   - Copiar ID de la URL
   - Compartir con el email del Service Account (como Editor)

3. **Crear pestañas en el Sheet:**
   - Pestaña 1: "POTENCIALES"
     - Columnas: NOMBRE, MUEBLE, FECHA_CONTACTO, ESTADO, QUIEN_LO_TIENE, TELEFONO, NOTA, FECHA_SEGUIMIENTO, VALOR_ESTIMADO
   - Pestaña 2: "PRODUCCION"
     - Columnas: ORDEN_ID, CLIENTE, MUEBLE, ESTADO, FECHA_INICIO, FECHA_ENTREGA_EST, PRODUCTOR, COSTO_REAL, PRECIO_FINAL, NOTAS_PRODUCCION

4. **Configurar Backend:**
   ```bash
   # Guardar JSON en backend/credentials/google-credentials.json
   # Actualizar .env:
   GOOGLE_SHEETS_ID=tu-sheet-id
   GOOGLE_CREDENTIALS_PATH=./credentials/google-credentials.json
   ```

5. **Probar:**
   ```bash
   python backend/test_google_sheets.py
   ```
   Debería mostrar:
   ```
   ✅ Google Sheets client initialized successfully!
   ✅ Sheet opened successfully!
   ✅ POTENCIALES sync successful
   ✅ PRODUCCION sync successful
   ```

---

## 📊 Ver Datos en Dashboards

Una vez que tengas datos (de prueba o Google Sheets):

1. **Página Potenciales:**
   - Tabla con todos los clientes
   - Filtros por estado
   - Botón para convertir a orden

2. **Página Producción:**
   - Tabla con todas las órdenes
   - Estados y fechas
   - Cálculo automático de días

3. **Página Dashboards:**
   - Gráfico Funnel (potenciales por estado)
   - Gráfico de Valor (estimado por estado)
   - Timeline de próximas entregas
   - KPIs consolidados (conversion rate, ingresos, etc)

---

## 🛠 Troubleshooting Rápido

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError: No module named 'gspread'` | Ejecutar `pip install -r requirements.txt` |
| `Cannot connect to http://localhost:8000` | Verificar que backend esté running en otra terminal |
| `GOOGLE_SHEETS_ID not set` | Agregar `GOOGLE_SHEETS_ID=...` al .env |
| `Google credentials not found` | Poner JSON en `backend/credentials/google-credentials.json` |
| `Permission denied` | Compartir Sheet con email del Service Account |
| Tabla vacía en React | Esperar 10-15 segundos (intervalo de sync) o agregar datos manualmente |

---

## 📝 Próximos Pasos

1. ✅ Instalar y ejecutar (arriba)
2. ⏭️ Probar con datos de prueba
3. ⏭️ Conectar Google Sheets (opcional)
4. ⏭️ Agregar más potenciales/órdenes
5. ⏭️ Usar la aplicación en producción

---

## 💡 Tips

- **Auto-refresh:** Los datos se actualizan automáticamente cada 30 segundos en frontend
- **Google Sheets sync:** Cada 10 minutos automáticamente
- **Desarrollo:** El servidor se reinicia automático al cambiar archivos (.py o .tsx)
- **Base de datos:** SQLite local en `backend/data/agency.db`

---

## 📚 Documentación Completa

- Backend: `backend/GOOGLE_SHEETS_SETUP.md`
- Código: `POLT_MOBILIER_SETUP.md`
- API Docs: http://localhost:8000/docs

¡Listo! 🎉 El sistema está funcionando. Ahora solo falta agregar datos y disfrutar de los dashboards.
