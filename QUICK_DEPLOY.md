# ⚡ Deploy Rápido - Polt Mobilier

## Opción 1: Deploy a Railway (RECOMENDADO - 3 clicks)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https%3A%2F%2Fgithub.com%2Fpabloalfon1223%2Fai-marketing-agency&envs=ANTHROPIC_API_KEY&ANTHROPIC_API_KEY=desc)

**Pasos:**
1. Haz click en el botón "Deploy on Railway" arriba
2. Autoriza con tu GitHub
3. Completa las variables de entorno:
   - `ANTHROPIC_API_KEY`: Tu clave de Anthropic
   - `GOOGLE_SHEETS_ID`: ID de tu sheet
   - `GOOGLE_CREDENTIALS_JSON`: Credenciales JSON
4. Click "Deploy"
5. Railway te da la URL (ej: `https://backend-abc123.railway.app`)
6. Continúa en **PASO 2** abajo

---

## Opción 2: Deploy Manual a Railway (5 minutos)

Si el botón no funciona, sigue estos pasos:

### 1. Crear cuenta en Railway
- Ir a https://railway.app
- Click "Sign up with GitHub"
- Autorizar Railway

### 2. Crear proyecto
- Click "New Project" → "Deploy from GitHub"
- Seleccionar repo: `pabloalfon1223/ai-marketing-agency`
- Click "Deploy"

### 3. Agregar variables de entorno
- En Railway: Variables → Add
  ```
  ANTHROPIC_API_KEY=sk-ant-xxxxx
  CORS_ORIGINS=https://ai-marketing-agency.vercel.app,http://localhost:5173
  GOOGLE_SHEETS_ID=tu-id-aqui
  GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
  GMAIL_ENABLED=false
  ```
- Railway automáticamente detecta `DATABASE_URL` con PostgreSQL

### 4. Obtener URL del backend
- En Railway: Settings → Domains
- Copiar la URL (algo como: `https://backend-abc123.railway.app`)

---

## PASO 2: Conectar Frontend a Backend (2 minutos)

Una vez que Railway esté deployado con el backend, conecta el frontend:

### En Vercel Dashboard:
1. Ir a Settings → Environment Variables
2. Agregar 2 variables:
   ```
   VITE_API_URL = https://[tu-backend-url]
   VITE_WS_URL = wss://[tu-backend-url]
   ```
   (Ejemplo: `https://backend-abc123.railway.app`)

3. Click "Redeploy" en el proyecto
4. Esperar a que Vercel redeploy (1-2 minutos)

### ✅ Verificar que funciona:
- Ir a: https://ai-marketing-agency.vercel.app
- Debería cargar sin errores
- Las páginas POTENCIALES, PRODUCCION, DASHBOARDS deberían mostrardatos

---

## URLs Finales

**Frontend:** https://ai-marketing-agency.vercel.app  
**Backend Docs:** https://[tu-url-railway]/docs  
**Backend Health:** https://[tu-url-railway]/api/v1/potenciales  

---

## Variables de Entorno Explicadas

### `ANTHROPIC_API_KEY`
Tu clave de API de Anthropic. Obtén una en: https://console.anthropic.com

### `GOOGLE_SHEETS_ID`
El ID de tu Google Sheet de Polt Mobilier.  
(Está en la URL: `https://docs.google.com/spreadsheets/d/[AQUI_ESTA_EL_ID]/edit`)

### `GOOGLE_CREDENTIALS_JSON`
Credenciales de Google Service Account en formato JSON de UNA LÍNEA.
```
Obtén este archivo de Google Cloud:
1. Ir a https://console.cloud.google.com
2. Crear Service Account
3. Crear JSON key
4. Copiar TODO el contenido en UNA LÍNEA (sin saltos)
```

### `CORS_ORIGINS`
Vueltas permitidas para CORS. Vercel + localhost para testing.

---

## ❌ Si algo falla:

### Error: "Cannot connect to backend"
- Verificar que `VITE_API_URL` en Vercel es correcto
- Verificar que Railway está deployado
- Revisar logs en Railway Dashboard

### Error: "Database connection failed"
- Railway automáticamente crea PostgreSQL
- Si no aparece: agregar servicio PostgreSQL manualmente
- Verificar que `DATABASE_URL` está en variables

### Error: "Sheets sync failed"
- Verificar credenciales de Google
- Verificar que `GOOGLE_SHEETS_ID` es correcto
- Ver logs: Railway Dashboard → Logs

---

## Próximos Pasos Opcionales

Después de confirmar que todo funciona:

1. ✅ Setup Gmail notifications (GMAIL_* variables)
2. ✅ Conectar AppSheets para formularios móvil
3. ✅ Configurar alertas automáticas

Consulta `DEPLOYMENT.md` para detalles completos.

---

**¿Necesitas ayuda?** Consulta los logs:
- **Railway:** Railway Dashboard → Logs
- **Vercel:** Vercel Dashboard → Deployments → Logs
- **Frontend Console:** DevTools (F12) → Console
