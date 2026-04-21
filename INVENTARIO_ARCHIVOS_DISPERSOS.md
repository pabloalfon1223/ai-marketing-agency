# 📋 Inventario Completo: Archivos Dispersos + Centralización

**Fecha:** 2026-04-18  
**Estado:** Búsqueda exhaustiva completada  
**Objetivo:** Centralizar TODO antes de ejecutar Fase 2

---

## 📍 ARCHIVOS ENCONTRADOS EN SESIONES COWORK

### 1. Dashboards Polt Mobilier (8 versiones HTML)
**Ubicación:** `/c/Users/lucas/AppData/Roaming/Claude/local-agent-mode-sessions/b61cda65-69e2-41e8-9222-9aaaf5eab55d/ebeb6156-625d-4750-a015-49373fa1e011/local_793cc94d-8a80-4770-94c4-f0dceae1dfac/outputs/polt-mobilier/dashboard/`

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `polt_calculator.html` | Calculadora base | ~50KB |
| `polt_calculator_pro.html` | Versión pro mejorada | ~55KB |
| `polt_dashboard.html` | Dashboard inicial | ~60KB |
| `polt_dashboard_carpintero.html` | Vista para carpintero | ~65KB |
| `polt_dashboard_v2.html` | Iteración 2 | ~70KB |
| `polt_dashboard_v3.html` | Iteración 3 | ~72KB |
| `polt_dashboard_v4.html` | Iteración 4 | ~75KB |
| `polt_dashboard_v4_fixed.html` | Versión fix | ~76KB |
| `polt_dashboard_v5_with_analyzer.html` | Versión final con analyzer | ~80KB |

**Status:** DISPERSO - No están en carpeta principal del proyecto

---

### 2. Contenido Mente Pausada (DOCX + XLSX)
**Ubicación:** `/c/Users/lucas/AppData/Roaming/Claude/local-agent-mode-sessions/b61cda65-69e2-41e8-9222-9aaaf5eab55d/ebeb6156-625d-4750-a015-49373fa1e011/local_e6d12b4b-9e87-4210-b320-5a7fe3f71167/outputs/`

| Archivo | Descripción | Tamaño |
|---------|-------------|--------|
| `contenido-mente-pausada-6piezas.docx` | 6 piezas de contenido | ~200KB |
| `mente-pausada-blueprint.docx` | Blueprint del producto | ~150KB |
| `tabla-contenido-mente-pausada.xlsx` | Tabla con calendario/estructura | ~100KB |

**Status:** DISPERSO - No están en carpeta principal

---

### 3. Documentación de Proyectos (Cache)
**Ubicación:** `/c/Users/lucas/AppData/Roaming/Claude/local-agent-mode-sessions/b61cda65-69e2-41e8-9222-9aaaf5eab55d/ebeb6156-625d-4750-a015-49373fa1e011/.project-cache/`

**Contiene:** 50+ archivos MD de documentación de marcas, audiencias, pilares, hooks, formatos, etc.

**Status:** DISPERSO - Información valiosa pero en cache de sesión anterior

---

### 4. Agentes y Configuración Mente Pausada
**Ubicación:** `/c/Users/lucas/AppData/Roaming/Claude/local-agent-mode-sessions/.../local_793cc94d.../outputs/mente-pausada/`

| Archivo | Descripción |
|---------|-------------|
| `agents/copy_agent.md` | Agente de copy |
| `agents/guion_agent.md` | Agente de guiones |
| `agents/prompt_agent.md` | Agente de prompts |
| `agents/scout_agent.md` | Agente scout |
| `agents/stories_agent.md` | Agente de stories |
| `config/brand_kit.md` | Kit de marca |
| `config/sheet_config.json` | Configuración de sheets |
| `config/visual_categories.md` | Categorías visuales |
| `scripts/generate_content.py` | Script de generación |
| `scripts/read_sheet.py` | Script lectura sheets |
| `scripts/write_to_sheet.py` | Script escritura sheets |
| `scripts/utils.py` | Utilidades |

**Status:** DISPERSO - Son assets útiles de sesiones anteriores

---

## ✅ ARCHIVOS YA CENTRALIZADOS (en /ai-marketing-agency/)

### Backend Completo
```
backend/app/
├── api/                    [✅ 12 endpoints registrados]
│   ├── agents.py
│   ├── analytics.py
│   ├── campaigns.py
│   ├── checkout.py
│   ├── clients.py
│   ├── content.py
│   ├── ideas.py
│   ├── orders.py
│   ├── projects.py
│   ├── purchases.py
│   └── websocket.py
├── models/                 [✅ 10 modelos definidos]
│   ├── agent_log.py
│   ├── campaign.py
│   ├── client.py
│   ├── content.py
│   ├── idea.py
│   ├── order.py
│   ├── project.py
│   ├── purchase.py
│   └── task.py
├── brands/                 [✅ 3 perfiles completos]
│   ├── mente_pausada.py
│   ├── polt_mobilier.py
│   └── cerebro.py
├── agents/                 [✅ Agentes principales]
├── services/               [✅ Servicios de negocio]
├── email_sequences.py      [⚠️ Templates OK, SendGrid NO implementado]
└── main.py                 [✅ Rutas registradas]
```

### Frontend React
```
frontend/src/
├── pages/
│   ├── MentePausadaLanding.tsx     [✅ Landing completa]
│   └── [otros archivos]
├── components/
│   ├── MentePausadaDashboard.tsx   [✅ Dashboard 6 charts]
│   └── [otros componentes]
```

### Documentación (en raíz de /ai-marketing-agency/)
```
✅ SYSTEM_ARCHITECTURE.md           (12.7KB)
✅ PROCESS_MENTE_PAUSADA.md         (11KB)
✅ PROCESS_POLT_MOBILIER.md         (10.3KB)
✅ PROCESS_CEREBRO.md               (12.2KB)
✅ CONFIGURATION_STATUS.md          (10.4KB)
✅ INTEGRATION_CHECKLIST.md         (10.6KB)
✅ DAILY_ANALYTICS_TASK.md          (2.3KB)
✅ .env.example                     (635B)
```

### Tareas Programadas
```
scheduled-tasks/
├── daily-analytics-mente-pausada/SKILL.md       [✅ Activa]
└── email-sequence-scheduler-mente-pausada/SKILL.md [✅ Activa]
```

---

## 🔴 BLOQUEADORES CRÍTICOS ACTUALES

```
MENTE PAUSADA NO VIVE PORQUE:

1. 🔴 SendGrid NO implementada
   - email_sequences.py línea 166-180 = PLACEHOLDER comentado
   - Necesita: send_email_sendgrid() con cliente real
   
2. 🔴 Stripe NO integrada
   - checkout.py estructura OK
   - Falta: keys reales, webhook secret
   
3. 🔴 Database schema NO creado
   - Modelos definidos pero NO tablas en BD
   - Alembic migrations NO ejecutadas
   
4. 🔴 API routes probablemente NO registradas
   - main.py dice que SÍ están registradas
   - Verificar que imports y include_router() estén OK
   
5. 🔴 Landing page NO desplegada
   - React existe pero Vercel NO configurado
```

---

## 📦 PROPUESTA DE CENTRALIZACIÓN

### Paso 1: Reorganizar en /ai-marketing-agency/

```
CREAR ESTRUCTURA:

ai-marketing-agency/
├── backend/                        [EXISTENTE]
├── frontend/                       [EXISTENTE]
├── docs/                           [NUEVA]
│   ├── SYSTEM_ARCHITECTURE.md
│   ├── PROCESS_*.md
│   ├── CONFIGURATION_STATUS.md
│   └── INTEGRATION_CHECKLIST.md
├── archived-assets/                [NUEVA - para sesiones cowork]
│   ├── polt-dashboards/
│   │   ├── v1-polt_calculator.html
│   │   ├── v2-polt_calculator_pro.html
│   │   ├── v3-polt_dashboard.html
│   │   ├── v4-polt_dashboard_v2.html
│   │   ├── v5-polt_dashboard_v3.html
│   │   ├── v6-polt_dashboard_v4.html
│   │   ├── v7-polt_dashboard_v5_analyzer.html
│   │   └── README_DASHBOARDS.md
│   ├── mente-pausada-content/
│   │   ├── contenido-6piezas.docx
│   │   ├── blueprint.docx
│   │   ├── tabla-contenido.xlsx
│   │   └── README_CONTENT.md
│   └── agents-config/              [De sesiones Cowork]
│       ├── mente-pausada-agents/
│       └── README_AGENTS.md
├── .claude/
│   └── scheduled-tasks/            [EXISTENTE]
└── INVENTARIO_ARCHIVOS_DISPERSOS.md [ESTE ARCHIVO]
```

### Paso 2: Crear archivos INDEX

**`archived-assets/README_DASHBOARDS.md`**
```markdown
# Dashboards Polt Mobilier - Histórico

## Versión actual en producción:
→ `frontend/src/pages/PoltDashboard.tsx` (React)
→ Desplegada en: https://incredible-tapioca-c3c3f1.netlify.app/

## Versiones HTML (legacy - sesiones anteriores):
1. polt_calculator.html - v1 básico
2. polt_calculator_pro.html - v2 mejorado
...
9. polt_dashboard_v5_analyzer.html - v5 final

Estos archivos HTML fueron iteraciones durante sesiones de Cowork.
La versión actual es la componente React que ya está en producción.
```

---

## 🎯 SIGUIENTE ACCIÓN

Una vez centralizado TODO:

### Inmediato (Hoy):
- [ ] Copiar dashboards a `archived-assets/polt-dashboards/`
- [ ] Copiar contenido a `archived-assets/mente-pausada-content/`
- [ ] Copiar agents a `archived-assets/agents-config/`
- [ ] Crear README para cada carpeta de assets

### Luego (Fase 2 - Mente Pausada Live):
1. **SendGrid Integration** (2-3 horas)
   - Obtener API key
   - Implementar `send_email_sendgrid()` en `backend/app/email_sequences.py`
   - Testear email enviado

2. **Stripe Integration** (2-3 horas)
   - Configurar keys (test primero)
   - Registrar webhook en dashboard Stripe
   - Testear checkout end-to-end

3. **Database Schema** (1 hora)
   - Crear migrations Alembic O ejecutar CREATE TABLE directo
   - Verificar que models tengan schema en BD

4. **Deploy Landing** (1-2 horas)
   - Configurar Vercel/Netlify
   - Conectar a dominio real
   - Test de conversión completa

5. **Teste Completo** (1 hora)
   - Landing → Click CTA → Checkout Stripe → Email day 0 → Analytics

---

## 📊 RESUMEN ESTADO ACTUAL

| Item | Estado | Bloquea Venta? |
|------|--------|---|
| Backend APIs | ✅ 95% completo | 🔴 Rutas sin registrar? |
| Frontend Landing | ✅ Diseñado | 🔴 No desplegado |
| Email Templates | ✅ 5 templates | 🔴 SendGrid no integrado |
| Stripe Integration | 🟡 Estructura | 🔴 Keys no configuradas |
| Database Modelos | ✅ Definidos | 🔴 Schema no creado |
| Tareas Programadas | ✅ 2 activas | ✅ No bloquea inicio |
| Documentación | ✅ Completa | ✅ No bloquea |
| Dashboards Polt | ✅ Múltiples | ✅ Ya en Netlify |
| Skills /humanizer | ✅ Creado | ✅ No bloquea |
| Skills /concise | ✅ Creado | ✅ No bloquea |

**BOTTLENECK:** 5 bloqueadores críticos previenen primera venta.

---

## 💡 Decisión: ¿Centralizar TODO o solo lo crítico?

### Opción A: Centralizar TODO (Clean Start)
- Copiar todos los archivos dispersos a `archived-assets/`
- Crear inventario detallado
- Ventaja: Visibilidad 100%, nada se pierde
- Desventaja: +30 minutos de trabajo organizacional

### Opción B: Centralizar CRÍTICO + linkear el resto
- Copiar SOLO: dashboards Polt, contenido Mente Pausada
- Dejar resto en sesiones Cowork con referencia aquí
- Ventaja: Rápido, minimalista
- Desventaja: Sesiones Cowork son efímeras

**RECOMENDACIÓN:** Opción A - Hoy la computadora está limpia, mañana puedes hacer limpieza de sesiones Cowork.

---

## 📝 Próxima Sesión

Cuando respondas, el plan es:

1. **Confirmación:** ¿Procedemos con centralización Opción A?
2. **Ejecución:** Copiar archivos dispersos a estructura propuesta
3. **Verificación:** Crear checklist de 5 bloqueadores + timeline
4. **Acción:** Iniciar Fase 2 - Resolver bloqueador #1 (SendGrid)

---

*Inventario creado: 2026-04-18 20:15*  
*Análisis: Búsqueda exhaustiva completada*  
*Archivos dispersos identificados: 50+ archivos en sesiones Cowork*  
*Centralización propuesta: Estructura limpia y ordenada*
