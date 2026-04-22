# Deploy Backend en Render.com (GRATIS)

## ✅ Ventajas de Render vs Railway
- **100% GRATIS** (no tiene tier de pago)
- Soporta Python/FastAPI nativamente
- Sleep gratuito después de 15min inactividad (despierta al recibir request)
- Almacenamiento gratuito

## 📋 Pasos de Deploy

### 1. Crear cuenta en Render
1. Ir a https://render.com
2. Click en "Sign Up"
3. Conectar con GitHub (usa tu cuenta)
4. Autorizar acceso al repositorio `pabloalfon1223/ai-marketing-agency`

### 2. Crear nuevo servicio web
1. En dashboard de Render, click "New +" → "Web Service"
2. Seleccionar repositorio: `ai-marketing-agency`
3. Rama: `main`
4. Configurar:
   - **Name**: `ai-marketing-agency-backend`
   - **Runtime**: `Python 3.11`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free (100% gratis)

### 3. Agregar variables de entorno
En la sección "Environment", agregar:

- `ANTHROPIC_API_KEY`: tu API key de Anthropic
- `CORS_ORIGINS`: `https://ai-marketing-agency-ruby.vercel.app,http://localhost:5173`
- `GOOGLE_SHEETS_ID`: tu Google Sheets ID (opcional por ahora)
- `GOOGLE_CREDENTIALS_JSON`: credenciales JSON (opcional por ahora)
- `GMAIL_ENABLED`: `false`

### 4. Deploy
Click en "Create Web Service"
- Esperar 3-5 minutos mientras construye y despliega
- Te dará una URL como: `https://ai-marketing-agency-backend.onrender.com`

### 5. Conectar frontend a backend en Vercel

Una vez que Render diga "Live" (✅):

```bash
cd "C:\Users\lucas\.claude\CLAUDE\ai-marketing-agency"
vercel env add VITE_API_URL https://ai-marketing-agency-backend.onrender.com
vercel --prod
```

---

## ✅ Verificar que funciona

Una vez deployado, probar:
```
https://ai-marketing-agency-backend.onrender.com/api/v1/health
```

Debería responder:
```json
{"status": "ok", "service": "AI Marketing Agency"}
```

---

## 💡 Notas
- Render tiene "sleep" después de 15 min sin tráfico (plan gratis)
- Despierta automáticamente al recibir un request
- Si quieres evitar sleep, actualiza a plan pago ($7/mes)
- Para desarrollo, esto es más que suficiente
