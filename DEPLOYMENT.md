# Guía de Deployment - Polt Mobilier

## Arquitectura Actual
- **Frontend**: React/TypeScript en Vercel ✅
- **Backend**: FastAPI en Railway (necesario)
- **Base de datos**: PostgreSQL en Railway (automático)
- **Google Sheets**: Sincronización cada 10 minutos

## Estado Actual
- ✅ Frontend deployed a Vercel: https://ai-marketing-agency.vercel.app
- ❌ Backend no deployado (solo localhost:8000)
- ❌ Falta conectar Frontend → Backend

---

## PASO 1: Deployar Backend a Railway

### 1.1 Crear cuenta en Railway (5 min)
1. Ir a https://railway.app
2. Click en "Sign up with GitHub"
3. Autorizar Railway para acceder a tus repos
4. Completar setup

### 1.2 Crear nuevo proyecto en Railway
1. Click en "New Project"
2. Seleccionar "Deploy from GitHub"
3. Buscar y seleccionar el repo `ai-marketing-agency`
4. Railway automáticamente detectará que es una app Python

### 1.3 Configurar variables de entorno en Railway
Railway proporciona automáticamente `DATABASE_URL` con PostgreSQL.

Necesitas agregar manualmente en Railway Dashboard → Project Settings → Variables:

```
ANTHROPIC_API_KEY=tu-clave-aqui
CORS_ORIGINS=https://ai-marketing-agency.vercel.app,http://localhost:5173
GOOGLE_SHEETS_ID=tu-sheet-id-aqui
GOOGLE_CREDENTIALS_JSON=tu-credenciales-json-aqui
GMAIL_ENABLED=false
```

#### Notas importantes:
- **ANTHROPIC_API_KEY**: Tu clave de API de Anthropic
- **CORS_ORIGINS**: URLs del frontend (Vercel + localhost para testing)
- **GOOGLE_SHEETS_ID**: El ID de tu Google Sheet de Polt Mobilier
- **GOOGLE_CREDENTIALS_JSON**: Tus credenciales de Google (en formato JSON string)
  - Para obtenerlo: descarga el JSON de Google Cloud y cópialo como string de una línea
  - O usa la alternativa: `GOOGLE_CREDENTIALS_PATH` con ruta al archivo (menos recomendado)

### 1.4 Deploy automático
Railway hace deploy automático cuando hace push a GitHub en la rama `main`.

1. El Procfile se encuentra en `backend/Procfile` y ya está configurado
2. Railway ejecutará: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
3. Railway proporciona automáticamente la URL (ej: `https://backend-abc123.railway.app`)

### 1.5 Verificar el deploy
Una vez deployed:
1. Railway te mostrará la URL del backend
2. Haz una request a: `https://tu-backend-url/docs` (Swagger UI)
3. Deberías ver la documentación interactiva de FastAPI

---

## PASO 2: Actualizar Frontend para conectar al Backend

### 2.1 Agregar variable de entorno en Vercel
1. Ir a Vercel Dashboard → Proyecto → Settings → Environment Variables
2. Agregar:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://tu-backend-url-railway`
   - **Environments**: Production, Preview, Development

Ejemplo:
```
VITE_API_URL=https://backend-abc123.railway.app
VITE_WS_URL=wss://backend-abc123.railway.app
```

### 2.2 Redeploy Frontend en Vercel
1. En Vercel Dashboard, click en "Redeploy" del proyecto
2. Vercel automáticamente usará la nueva variable de entorno `VITE_API_URL`

---

## PASO 3: Testear la integración

### 3.1 Acceder a la app
1. Ir a https://ai-marketing-agency.vercel.app
2. Debería cargar correctamente (sin errores 404)
3. Las páginas POTENCIALES, PRODUCCION, DASHBOARDS deberían funcionar

### 3.2 Testear conexión al backend
1. Abrir DevTools → Console
2. Deberías ver que carga datos de `/api/v1/potenciales`
3. Si hay errores CORS, revisar CORS_ORIGINS en Railway

### 3.3 Testear sincronización con Google Sheets
1. El backend intenta sincronizar cada 10 minutos
2. Ver logs en Railway Dashboard → Logs para confirmar que la sincronización funciona
3. Hacer un cambio en Google Sheets
4. Esperar 10 minutos
5. El cambio debería aparecer en la app

---

## TROUBLESHOOTING

### Error: "Cannot reach backend" en frontend
**Causa**: CORS_ORIGINS no incluye la URL de Vercel
**Solución**: 
1. En Railway Dashboard, actualizar `CORS_ORIGINS` a: `https://ai-marketing-agency.vercel.app,http://localhost:5173`
2. Redeploy el backend

### Error: "Database connection failed"
**Causa**: DATABASE_URL no está configurada
**Solución**:
1. Railway proporciona DATABASE_URL automáticamente
2. Si no aparece, crear un servicio PostgreSQL: click "Add Service" → "PostgreSQL"
3. Railway vincula automáticamente DATABASE_URL

### Error: "Google Sheets sync failed"
**Causa**: Credenciales de Google incorrectas
**Solución**:
1. Verificar que `GOOGLE_SHEETS_ID` es correcto
2. Verificar que `GOOGLE_CREDENTIALS_JSON` está bien formateado
3. Ver logs en Railway para detalles del error

### Error: "404 on Vercel"
**Causa**: Frontend no está sirviendo correctamente
**Solución**: Ya solucionado con `vercel.json`. Si persiste:
1. Revisar que `vercel.json` existe en `frontend/`
2. Revisar Build Logs en Vercel Dashboard
3. Hacer un "Redeploy" forzado

---

## Variables de Entorno Resumen

### Backend (Railway)
```
DATABASE_URL=postgresql://...  # Auto-provided by Railway
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx
CORS_ORIGINS=https://ai-marketing-agency.vercel.app,http://localhost:5173
GOOGLE_SHEETS_ID=abc123xyz...
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
GMAIL_ENABLED=false
GMAIL_SENDER_EMAIL=
GMAIL_APP_PASSWORD=
GMAIL_RECIPIENT_EMAIL=
```

### Frontend (Vercel)
```
VITE_API_URL=https://backend-abc123.railway.app
VITE_WS_URL=wss://backend-abc123.railway.app
```

---

## URLs Referencias
- Frontend: https://ai-marketing-agency.vercel.app
- Backend Docs (cuando esté deployado): https://tu-backend-url/docs
- Railway Dashboard: https://railway.app/dashboard
- Vercel Dashboard: https://vercel.com/dashboard

---

## Próximos Pasos Después del Deploy
1. ✅ Backend deployado a Railway
2. ✅ Frontend conectado al backend
3. Test end-to-end: Cambiar POTENCIAL a CLIENTE → debe crear automáticamente en PRODUCCION
4. Configurar Gmail notifications (opcional)
5. Configurar AppSheets para formularios móvil (opcional)
6. Monitorear logs en Railway para debugging

---

**Última actualización**: 2026-04-21
**Estado**: Guía inicial completada. Falta ejecutar deployment.
