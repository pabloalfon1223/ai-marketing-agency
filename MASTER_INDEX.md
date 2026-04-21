# 🧠 MASTER INDEX — SISTEMA COMPLETO
**Actualizado:** 2026-04-18  
**Carpeta raíz:** `C:\Users\lucas\.claude\CLAUDE\ai-marketing-agency\`

---

## 📍 CÓMO USAR ESTE ÍNDICE

Antes de trabajar en cualquier proyecto, leer:
1. Este archivo → entender dónde está todo
2. El plan detallado del proyecto → `PLAN_[PROYECTO]_DETALLADO.md`
3. El brand kit del proyecto → carpeta `[PROYECTO]/brand-kit/`

---

## 🗂️ ESTRUCTURA COMPLETA

```
ai-marketing-agency/
│
├── 📄 MASTER_INDEX.md          ← ESTÁS AQUÍ
├── 📄 RESUMEN_EJECUTIVO.md     ← Estado general + decisiones
├── 📄 PLAN_MENTE_PAUSADA_DETALLADO.md
├── 📄 PLAN_POLT_MOBILIER_DETALLADO.md
├── 📄 PLAN_CEREBRO_DETALLADO.md
│
├── 📂 MENTE-PAUSADA/           ← Todo de Mente Pausada
├── 📂 POLT-MOBILIER/           ← Todo de Polt Mobilier
├── 📂 CEREBRO/                 ← Todo de Cerebro
├── 📂 VENTURE-OS/              ← Sistema maestro de agentes
├── 📂 brand-briefs/            ← Skills de marketing (32+)
├── 📂 backend/                 ← Código FastAPI
└── 📂 frontend/                ← Código React
```

---

## 🧠 MENTE PAUSADA

**Landing activa:** `ruidomentalcero.lovable.app`  
**Producto:** Ruido Mental Cero — protocolo 7 noches audio guiado  
**Precio:** $99 (basic) / $149 (plus) / $199 (VIP)  
**Plataformas:** Instagram, TikTok  
**ManyChat trigger:** PAUSA → ruidomentalcero.lovable.app

### Archivos clave:
| Archivo | Descripción |
|---------|-------------|
| `PLAN_MENTE_PAUSADA_DETALLADO.md` | Plan completo + gaps a resolver |
| `MENTE-PAUSADA/brand-kit/00_kit_de_marca.md` | Índice del kit de marca |
| `MENTE-PAUSADA/brand-kit/01_identidad_de_marca.md` | Voz, tono, valores |
| `MENTE-PAUSADA/brand-kit/02_audiencia_objetivo.md` | Avatares, dolores, deseos |
| `MENTE-PAUSADA/brand-kit/03_pilares_de_contenido.md` | 6 pilares + distribución |
| `MENTE-PAUSADA/brand-kit/04_biblioteca_de_hooks.md` | Hooks por emoción |
| `MENTE-PAUSADA/brand-kit/05_formatos_y_estructura.md` | Reel, Carrusel, B-Roll |
| `MENTE-PAUSADA/brand-kit/06_sistema_de_conversion.md` | Embudo 3 capas + ManyChat |
| `MENTE-PAUSADA/brand-kit/07_guia_visual.md` | Paleta, tipografía, música |
| `MENTE-PAUSADA/brand-kit/08_limites_eticos.md` | Guardarails éticos |
| `MENTE-PAUSADA/brand-kit/brand_kit_v2.md` | Brand kit técnico (colores hex, vocab) |
| `MENTE-PAUSADA/brand-kit/visual_categories.md` | Categorías visuales para IA |

### Agents disponibles:
| Agent | Función |
|-------|---------|
| `MENTE-PAUSADA/agents/copy_agent.md` | Genera copy de contenido |
| `MENTE-PAUSADA/agents/guion_agent.md` | Genera guiones de Reels |
| `MENTE-PAUSADA/agents/prompt_agent.md` | Genera prompts visuales IA |
| `MENTE-PAUSADA/agents/scout_agent.md` | Detecta trends y oportunidades |
| `MENTE-PAUSADA/agents/stories_agent.md` | Genera Stories |

### Scripts Python:
| Script | Función |
|--------|---------|
| `MENTE-PAUSADA/scripts/generate_content.py` | Generación de contenido |
| `MENTE-PAUSADA/scripts/read_sheet.py` | Leer Google Sheets |
| `MENTE-PAUSADA/scripts/write_to_sheet.py` | Escribir en Google Sheets |
| `MENTE-PAUSADA/scripts/utils.py` | Utilidades comunes |

### ❌ GAPS PENDIENTES (Chat 1):
1. **SendGrid** no implementado → `backend/app/email_sequences.py` líneas 166-180
2. **Landing no desplegada** → Existe en React, falta deploy a Vercel
3. **Stripe keys** no configuradas → `.env` vacío

---

## 🛋️ POLT MOBILIER

**Calculadora activa:** `https://incredible-tapioca-c3c3f1.netlify.app/`  
**Producto:** Muebles 100% a medida  
**Precio:** $500–$5.000 por orden  
**Segmento:** Medio-premium, mujeres 28-45 Argentina

### Archivos clave:
| Archivo | Descripción |
|---------|-------------|
| `PLAN_POLT_MOBILIER_DETALLADO.md` | Plan completo + 6 gaps a resolver |
| `POLT-MOBILIER/brand-docs/BRAND_GUIDELINES_POLT_MOBILIER.md` | Brand completo (identidad, público, tono) |
| `POLT-MOBILIER/SISTEMA_COMPLETO_AUTOMATIZADO_POLT.md` | Flujo semanal 70 min (vs 600 manual) |
| `POLT-MOBILIER/PLAN_CONTENIDO_30DIAS_POLT_MOBILIER.md` | Plan de contenido mensual |
| `POLT-MOBILIER/RESUMEN_EJECUTIVO_POLT_MOBILIER.md` | Estado actual del proyecto |
| `POLT-MOBILIER/ARQUITECTURA_AGENTES_POLT_MOBILIER.md` | 8 agentes identificados |
| `POLT-MOBILIER/ESTRUCTURA_EXCEL_POLT_OPTIMIZADA.md` | Estructura del Excel de trabajo |

### Contenido generado (ejemplos):
```
POLT-MOBILIER/contenido-generado/
├── TEST-CASE-1-REEL-PLACAR.md        ← Reel completo (hook+copy+prompt visual)
├── TEST-CASE-2-POST-SOCIAL-PROOF.md  ← Post de testimonio
├── TEST-CASE-3-CARRUSEL-PROCESO.md   ← Carrusel educativo proceso
├── LUNES-IDEAS-CRUDAS-04-14.md       ← Ideas de una semana real
├── LUNES-REPORTE-FINAL-COMPLETO.md   ← Reporte semanal completo
└── EJEMPLOS_CONTENIDO_POLT_MOBILIER.md ← 10+ ejemplos de piezas
```

### Assets visuales:
```
Imágenes y videos en: C:\Users\lucas\Desktop\Pm\
├── Gemini_Generated_Image_*.png  ← Muebles generados IA (20+ imágenes)
├── ChatGPT Image *.png           ← Renders de muebles
├── WhatsApp Image *.jpeg         ← Fotos reales de proyectos
└── Videos: Calidez_a_medida, Tu_living_tu_refugio
```

### ❌ GAPS PENDIENTES (Chat 2):
1. **Skill gestor-ordenes** no existe → Crear en `backend/app/agents/`
2. **Email automático por hito** → 5 emails ciclo de orden
3. **Dashboard BD** → Conectar HTML v5 a API real
4. **Contenido automático 9 AM** → Tarea programada pendiente
5. **Calculadora → BD** → Integrar POST endpoint

---

## 🧬 CEREBRO

**Objetivo:** Sistema de validación de ideas $20-50k/mes  
**Estado:** Arquitectura lista, código 0%

### Archivos clave:
| Archivo | Descripción |
|---------|-------------|
| `PLAN_CEREBRO_DETALLADO.md` | Plan completo con arquitectura |
| `CEREBRO/skills/market-money-finder-SKILL.md` | Skill para encontrar oportunidades |
| `CEREBRO/skills/monetization-orchestrator-SKILL.md` | Skill para orquestar monetización |
| `CEREBRO/skills/opportunity-execution-commander-SKILL.md` | Skill para ejecutar oportunidades |
| `CEREBRO/IMPLEMENTATION-GUIDE.md` | Guía de implementación |
| `CEREBRO/referencias/reporte-ingresos-digitales-2026.md` | Análisis de 7 modelos de ingreso |
| `CEREBRO/referencias/01_ANALISIS_OPORTUNIDADES_INGRESO_2024.md` | Análisis de oportunidades |
| `CEREBRO/referencias/03_QUICK_CASH_2K_OPPORTUNITIES.md` | Ideas rápidas para generar $2k |
| `CEREBRO/referencias/02_CHECKLIST_30_DIAS.md` | Checklist de 30 días |

### ❌ GAPS PENDIENTES (Chat 3):
1. **Skill generador-ideas** → `backend/app/agents/ideas_generator.py`
2. **Skill validador-mercado** → `backend/app/agents/market_validator.py`
3. **Dashboard React** → `frontend/src/pages/CerebroDashboard.tsx`
4. **Tarea weekly-trending** → Lunes 8 AM
5. **Tarea monthly-retrospective** → 1° mes 9 AM

---

## 🤖 VENTURE OS (Sistema de Agentes Maestro)

**Archivo:** `VENTURE-OS/VENTURE_OS_CLAUDE.md`

Sistema completo con 20+ agentes organizados en 6 capas:

| Capa | Agentes |
|------|---------|
| **INTELIGENCIA** | SCOUT, COMPETE, AUDIENCE, TREND |
| **PRODUCTO** | PRODUCT, CREATOR, PRICING |
| **MARCA** | BRAND, COPY, LANDING, SEO |
| **MARKETING** | CONTENT, EMAIL, ADS, FUNNEL |
| **VENTAS** | SALES, CHECKOUT, UPSELL |
| **OPERACIONES** | AUTO, ANALYTICS, FINANCE |

**Principios operativos clave:**
- FACELESS: Sin cara pública
- RECURRENTE: Siempre incluir ingreso mensual
- USD: Target global
- SIMPLE: Menos es más
- AUTOMATIZABLE: Todo delegable

**Stack tecnológico definido:**
```
Claude Code | Notion | N8N | Hotmart | ManyChat
ElevenLabs | Freepik | Runway/Kling | CapCut
Mailerlite/Resend | Lovable/Carrd
```

---

## 🛠️ SKILLS DE MARKETING (32+ referencias)

**Ubicación:** `brand-briefs/skills-references/`

Clasificados en 5 categorías:
```
📝 Contenido y copy (5): copywriting, social-content, cold-email, email-sequence, copy-editing
⚡ CRO (8): page-cro, form-cro, signup-flow, onboarding, paywall, popup, churn, referral
📣 Ads (4): paid-ads, ad-creative, ab-test, launch-strategy
🔍 SEO (6): ai-seo, programmatic-seo, seo-audit, site-architecture, schema-markup, competitor
💰 Estrategia (9): content-strategy, pricing-strategy, marketing-psychology, revops, etc.
```

---

## 💻 BACKEND (FastAPI)

**Ubicación:** `backend/app/`

```
API Routes:  checkout, purchases, orders, ideas, clients, projects, campaigns, content
Agents:      content_agent, analytics_agent, ads_strategy, email_marketing, etc.
Models:      Purchase, Order, Idea, Client, Campaign, Content
Brands:      mente_pausada.py, polt_mobilier.py, cerebro.py
Database:    SQLite (auto-crea en startup)
Email:       email_sequences.py (templates OK, sending PENDIENTE)
```

---

## 🎨 FRONTEND (React)

**Ubicación:** `frontend/`

```
Landing: MentePausadaLanding.tsx (completo, sin deploy)
Dashboard: 6 charts, analytics
Deploy: PENDIENTE (Vercel)
```

---

## 📊 ESTADO GLOBAL

| Proyecto | Completitud | Próximo paso | Chat |
|---------|------------|--------------|------|
| Mente Pausada | 95% | SendGrid + Deploy | Chat 1 |
| Polt Mobilier | 50% | Gestor-órdenes + Auto | Chat 2 |
| Cerebro | 5% | Skills + Dashboard | Chat 3 |

---

## 🚀 ORDEN DE EJECUCIÓN RECOMENDADO

```
SEMANA 1: Chat 1 → Mente Pausada LIVE ($99+ revenue)
SEMANA 2: Chat 2 → Polt Mobilier automatizado ($500+ /orden)
SEMANA 3+: Chat 3 → Cerebro validando ideas ($20k+ potencial)
```

---

*Última actualización: 2026-04-18*  
*Estado: TODO centralizado. Listo para ejecutar.*
