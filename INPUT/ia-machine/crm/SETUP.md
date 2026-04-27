# IA Machine — Setup en 4 pasos

## PASO 1 — Crear proyecto Supabase (5 min)

1. Ir a **supabase.com** → New Project
2. Nombre: `ia-machine` | Region: `South America (São Paulo)`
3. Guardar la contraseña en algún lugar seguro
4. Ir a **Settings → API** y copiar:
   - `Project URL` → pegar en `.env.local` como `NEXT_PUBLIC_SUPABASE_URL`
   - `anon public` key → pegar en `.env.local` como `NEXT_PUBLIC_SUPABASE_ANON_KEY`

## PASO 2 — Crear las tablas (2 min)

1. En Supabase → **SQL Editor → New query**
2. Copiar y pegar el contenido de `supabase/schema.sql`
3. Click **Run** — crea todas las tablas + datos iniciales

## PASO 3 — Configurar auth (2 min)

1. En Supabase → **Authentication → Email Templates**
   - Podés personalizar el email del magic link
2. En **Authentication → URL Configuration**:
   - Site URL: `https://tu-app.vercel.app` (o `http://localhost:3000` para desarrollo)
   - Redirect URLs: agregar `https://tu-app.vercel.app/**`

## PASO 4 — Deploy en Vercel (5 min)

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Desde la carpeta del CRM
cd "C:/Users/lucas/AppData/Roaming/Claude/CLAUDE/ia-machine/crm"
vercel

# 3. Seguir el wizard:
#    - Link to existing project? N
#    - Project name: ia-machine
#    - Framework: Next.js (detectado automático)

# 4. Agregar variables de entorno en Vercel Dashboard:
#    vercel.com → tu proyecto → Settings → Environment Variables
#    Agregar las 4 variables de .env.local
```

## Verificar que funciona

```bash
# Local
npm run dev
# → abrir http://localhost:3000
# → redirige a /login
# → ingresás lucasjolivera3@gmail.com
# → recibís el magic link
# → entrás al dashboard con datos reales
```

## Estructura de archivos clave

```
crm/
├── src/
│   ├── lib/
│   │   ├── supabase.ts   ← cliente + tipos
│   │   └── db.ts         ← todas las queries
│   ├── app/
│   │   ├── page.tsx      ← dashboard principal
│   │   ├── agents/       ← gestión de agentes
│   │   ├── contacts/     ← CRM de contactos
│   │   ├── login/        ← magic link auth
│   │   └── pipeline/     ← pipeline de ventas
│   └── middleware.ts     ← protección de rutas
└── supabase/
    └── schema.sql        ← estructura completa de la DB
```

## Cómo los agentes se auto-registran

Cualquier agente nuevo puede registrarse en la DB llamando a `upsertAgent()`:

```typescript
import { upsertAgent, startRun, finishRun } from "@/lib/db";

// El agente se registra solo la primera vez que corre
await upsertAgent({
  id: "mi-nuevo-agente",
  name: "Mi Nuevo Agente",
  description: "Hace X cosa para Y proyecto",
  project_id: "mente-pausada",
  schedule: "09:00 ARG",
});

// Registra el inicio
const runId = await startRun("mi-nuevo-agente", "mente-pausada", "schedule");

// ... hace su trabajo ...

// Registra el resultado
await finishRun(runId, "mi-nuevo-agente", "success", { resultado: "..." }, ["[09:00] Completado"]);
```
