# Sistema de Automatización Integral - Arquitectura

## 🎯 Visión General

Ecosistema semi-automatizado que genera ingresos de 3 proyectos independientes:

1. **Mente Pausada** - Ebook + audios de bienestar (one-time $99-199)
2. **Polt Mobilier** - Muebles personalizados (órdenes por encargo)
3. **Cerebro** - Ideas de negocio escalables ($20k-50k/mes)

Cada proyecto es **independiente en datos y lógica**, pero comparten:
- Scheduler maestro centralizado
- Dashboard de observación
- Learnings y tácticas que funcionan

---

## 📊 Stack Técnico

### Backend
- **Framework:** FastAPI (Python)
- **Base de datos:** SQLite (con SQLAlchemy ORM)
- **Task Queue:** Redis (opcional, para background jobs)
- **Emails:** SendGrid/SMTP (templates + automation)
- **Pagos:** Stripe (checkout + webhooks)
- **IA:** Claude API (agents y prompts)

### Frontend
- **Framework:** React + TypeScript
- **Gráficos:** Recharts (dashboards interactivos)
- **Deploy:** Netlify/Vercel
- **Diseño:** Tailwind CSS + color palettes por proyecto

### Automatización
- **Scheduler:** Claude Code scheduled tasks (5+ tareas diarias)
- **Flujo:** AI genera → Creador humano revisa → Auto-publica/vende
- **Observación:** Dashboards en tiempo real + reportes diarios

---

## 🧠 Mente Pausada - Flujo Completo

### Fases del Customer Journey

```
1. DISCOVERY (Marketing)
   └─ Ads (Meta/Google) → Landing page
   
2. DECISION (Venta)
   └─ Landing page → Stripe checkout → Compra registrada
   
3. ONBOARDING (Email Automation)
   └─ Day 0: Acceso + bienvenida
   └─ Day 3: Enseña técnica (4-7-8 breathing)
   └─ Day 7: Social proof (testimonios)
   └─ Day 10: Upsell (coaching $500 o comunidad)
   └─ Day 14: Feedback (encuesta satisfacción)
   
4. OBSERVE (Analytics)
   └─ 5 PM diariamente: Reporte de ingresos, conversión, ROAS
```

### Endpoints & Flujos

**Landing Page Flow**
```
GET /landing/mente-pausada
  ├─ Hero + problema
  ├─ 3 opciones de precio
  ├─ Testimonios/social proof
  ├─ FAQ
  └─ CTA: "Comprar ahora"

POST /api/checkout/create-session
  ├─ Input: producto (basic/plus/vip) + email
  ├─ Output: Stripe session ID
  └─ Redirect a Stripe

Stripe Webhook: POST /api/webhook/stripe
  ├─ Event: payment_intent.succeeded
  ├─ Acción: Crear record de Purchase en BD
  ├─ Acción: Enviar email day_0
  └─ Acción: Generar download link
```

**Analytics Flow**
```
GET /api/analytics/mente-pausada?range=7d|30d|90d
  ├─ Revenue: suma de purchases
  ├─ Conversión: purchases / visits (UTM tracking)
  ├─ AOV: revenue / purchases
  ├─ ROAS: revenue / ad_spend
  ├─ LTV: estimado basado en upsells históricos
  └─ Tier breakdown: cuántas compras por precio

Scheduled Task (5 PM daily): DAILY_ANALYTICS_TASK
  ├─ Query últimas 24h de purchases
  ├─ Calcula métricas (hoy, 7d, 30d)
  ├─ Genera recomendaciones automáticas
  └─ Guarda report en /output/analytics-{DATE}.md
```

**Email Sequence Flow**
```
Event: Purchase created (day 0)
  ├─ day_0 (5 min): Welcome + acceso
  ├─ day_3 (72h): Enseña 4-7-8 breathing
  ├─ day_7 (168h): Social proof
  ├─ day_10 (240h): Upsell coaching/community
  └─ day_14 (336h): Feedback survey

Scheduled Task (4x daily): EMAIL_SEQUENCE_SCHEDULER
  ├─ Query purchases con días pendientes
  ├─ Si hoy es day_X: envía email_X
  ├─ Actualiza purchase.email_sequence_status
  └─ Registra en log
```

### Base de Datos

**Tabla: purchases**
```sql
CREATE TABLE purchases (
  id INTEGER PRIMARY KEY,
  email VARCHAR(255) UNIQUE,
  product_tier VARCHAR(20),  -- basic/plus/vip
  amount DECIMAL(10,2),
  currency VARCHAR(3),  -- USD/ARS
  payment_status VARCHAR(20),  -- pending/success/failed
  purchase_date DATETIME,
  
  -- Email sequence tracking
  email_sequence_status VARCHAR(20),  -- day_0/day_3/day_7/day_10/day_14
  last_email_sent_at DATETIME,
  email_sent_count INTEGER DEFAULT 0,
  
  -- Analytics tracking
  utm_source VARCHAR(100),  -- meta/google/organic/direct
  utm_campaign VARCHAR(100),
  
  -- Download access
  access_token VARCHAR(255),
  access_expires_at DATETIME
)
```

---

## 🛋️ Polt Mobilier - Flujo Completo

### Fases del Customer Journey

```
1. DISCOVERY (Marketing)
   └─ Content (9 AM diario) → Instagram/email
   └─ Calculadora web → Lead capture
   
2. CONSULTA (Order creation)
   └─ Cliente solicita presupuesto → Skill gestión de órdenes
   └─ Genera propuesta personalizada
   
3. PRODUCCIÓN (Orden workflow)
   └─ Orden registrada → Asignación taller
   └─ Progreso diario → Notificaciones cliente
   
4. ENTREGA (Fulfillment)
   └─ Coordinación entrega
   └─ Encuesta satisfacción
   
5. OBSERVE (Analytics)
   └─ 5 PM diariamente: Órdenes en curso, retrasos
```

### Endpoints & Flujos

**Order Creation Flow**
```
POST /api/orders/create
  ├─ Input: customer email, producto, specs
  ├─ Output: order_number, ETA
  ├─ Skill: gestión-ordenes-polt
  │  ├─ Analiza specs → estima costo
  │  ├─ Genera propuesta personalizada
  │  └─ Asigna a productor disponible
  └─ Acción: Envía email confirmación

PUT /api/orders/{id}/status
  ├─ Input: nuevo status (En progreso/Casi listo/Listo)
  ├─ Acción: Notifica cliente vía email/WhatsApp
  └─ Acción: Guarda foto de progreso si aplica
```

**Content Generation Flow**
```
Scheduled Task (9 AM daily): DAILY_CONTENT_POLT
  ├─ Genera 3-5 piezas Instagram (videos, carruseles)
  ├─ Genera email newsletter (proyectos, tips)
  ├─ Creador humano revisa y aprueba
  └─ Auto-publica en redes
```

### Base de Datos

**Tabla: orders**
```sql
CREATE TABLE orders (
  id INTEGER PRIMARY KEY,
  order_number VARCHAR(20) UNIQUE,  -- POL-20260417-001
  customer_email VARCHAR(255),
  customer_name VARCHAR(255),
  
  -- Producto
  product_type VARCHAR(100),  -- silla, mesa, estantería
  custom_specs TEXT,  -- medidas, material, estilo
  
  -- Costos
  estimated_cost DECIMAL(10,2),
  final_cost DECIMAL(10,2),
  payment_status VARCHAR(20),  -- pending/paid/delivered
  
  -- Producción
  status VARCHAR(20),  -- en_espera/en_progreso/casi_listo/listo/entregado
  assigned_producer VARCHAR(255),
  start_date DATETIME,
  estimated_delivery DATETIME,
  actual_delivery DATETIME,
  
  -- Comunicación
  email_sent_count INTEGER,
  last_notification_at DATETIME,
  work_photos TEXT  -- array of photo URLs
)
```

---

## 🧬 Cerebro - Flujo Completo

### Fases de Validación de Ideas

```
1. IDEACIÓN (Generación)
   └─ Skill: generador-ideas-cerebro
   └─ Input: tiempo disponible, capital, skills
   └─ Output: 20+ ideas ranqueadas

2. VALIDACIÓN (Scoring)
   └─ Skill: validador-mercado-cerebro
   └─ Analiza: demanda, competencia, viabilidad
   └─ Score: 0-100 (demanda 40%, escalabilidad 40%, competencia 20%)

3. MVP (Lanzamiento rápido)
   └─ Idea con score >70: crear MVP mínimo
   └─ Timeline: validar en $500/mes antes de escalar a $20k

4. OBSERVE (Tracking)
   └─ Semanal: trending ideas, nuevas validaciones
   └─ Mensual: retrospectiva, decisiones
```

### Endpoints & Flujos

**Idea Generation Flow**
```
POST /api/ideas/generate
  ├─ Input: capital_available, time_available, skills
  ├─ Skill: generador-ideas-cerebro (Claude)
  │  ├─ Busca trending topics
  │  ├─ Genera 20+ ideas por tipo (SaaS, servicios, etc)
  │  └─ Rankea por potencial ($20k/mes)
  └─ Output: ideas con descripción y score estimado

PUT /api/ideas/{id}/validate
  ├─ Skill: validador-mercado-cerebro
  │  ├─ Google Trends, Reddit, Quora, ProductHunt
  │  ├─ Análisis competencia
  │  ├─ TAM (total addressable market)
  │  └─ Cálculo de score final
  └─ Output: Viability score + recomendaciones
```

**Analytics Flow**
```
Scheduled Task (Lunes 8 AM): WEEKLY_TRENDING_IDEAS
  ├─ Revisa Google Trends, ProductHunt, LinkedIn, TikTok
  ├─ Identifica 10 nuevas ideas trending
  ├─ Descarta ideas con demanda en caída
  └─ Genera: Weekly opportunity report

Scheduled Task (1° de mes): CEREBRO_RETROSPECTIVE
  ├─ Analiza: ideas que fallaron, por qué
  ├─ Decisiones: pivotar vs descartar vs invertir
  ├─ Propone: 3 ideas para enfoque próximo mes
  └─ Registra learnings compartibles con otros proyectos
```

### Base de Datos

**Tabla: ideas**
```sql
CREATE TABLE ideas (
  id INTEGER PRIMARY KEY,
  title VARCHAR(255),
  description TEXT,
  idea_type VARCHAR(50),  -- saas/servicios/ecommerce/creator/hybrid
  
  -- Validación
  demand_score INTEGER (0-100),
  scalability_score INTEGER (0-100),
  competition_score INTEGER (0-100),
  overall_score INTEGER (0-100),
  
  -- Evidencia
  demand_evidence TEXT,  -- URLs, trending keywords
  competitor_evidence TEXT,  -- qué existe, pricing, gaps
  
  -- MVP
  mvp_outline TEXT,  -- qué es lo mínimo para validar
  estimated_time_to_validate INTEGER,  -- días
  estimated_capital_needed DECIMAL(10,2),
  
  -- Lifecycle
  status VARCHAR(20),  -- idea_cruda/validada/mvp_lanzado/en_track_20k/exitosa/pivotada/descartada
  validation_date DATETIME,
  launch_date DATETIME,
  
  -- Revenue tracking
  current_monthly_revenue DECIMAL(10,2),
  reached_20k BOOLEAN,
  
  -- Learnings
  learnings TEXT,
  pivot_reason TEXT
)
```

---

## 🎛️ Dashboard Central

### Observación (No Control)

**Home Dashboard**
```
┌─────────────────────────────────────────────────┐
│ INGRESOS TOTALES: $XXX (últimos 30 días)        │
├─────────────────────────────────────────────────┤
│ Mente Pausada: $XXX (X% del total)              │
│ Polt Mobilier: $XXX (X% del total)              │
│ Cerebro: $XXX (X% del total)                    │
├─────────────────────────────────────────────────┤
│ TENDENCIA: ↑ +X% vs. mes anterior               │
│ META MENSUAL: En track para $XXX (target $XXXX) │
└─────────────────────────────────────────────────┘
```

**Mente Pausada Dashboard**
```
KPIs:
- Total Revenue | AOV | Conversion Rate | Daily Avg
- Revenue chart (7d/30d/90d)
- Tier breakdown (pie chart: Basic/Plus/VIP)
- Daily purchases (bar chart)
- Conversion rate % (line chart)
- Insights & recommendations (4 cards)
```

**Polt Mobilier Dashboard**
```
KPIs:
- Active Orders | Avg Order Value | Production Status | Satisfaction
- Orders in progress
- Production timeline
- Customer notifications sent
- Revenue this month
```

**Cerebro Dashboard**
```
KPIs:
- Ideas scored | Ideas validated | In MVP | Revenue $20k+
- Ideas table: title, score, type, status, revenue
- Filters: by score, by type, by capital required
- Trending ideas this week
- Opportunities ranked by viability
```

---

## 📅 Tareas Programadas (5+ diarias)

| Tarea | Hora | Frecuencia | Proyecto |
|-------|------|-----------|----------|
| `daily-content-ideas` | 7 AM | Diariamente | General |
| `daily-content-polt` | 9 AM | Diariamente | Polt |
| `daily-analytics-mente-pausada` | 5 PM | Diariamente | Mente Pausada |
| `email-sequence-scheduler` | 3 AM, 9 AM, 3 PM, 9 PM | 4x diarios | Mente Pausada |
| `weekly-trending-ideas` | Lunes 8 AM | Semanalmente | Cerebro |
| `cerebro-monthly-retrospective` | 1° mes 9 AM | Mensualmente | Cerebro |
| `daily-polt-analytics` | 5 PM | Diariamente | Polt |

---

## 🔐 Seguridad & Configuración

### Variables de Entorno (.env)
```
# Stripe
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email
SENDGRID_API_KEY=SG.xxx
SENDER_EMAIL=hola@mentepausada.com

# IA
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# Server
DOMAIN_URL=https://mentepausada.com
CORS_ORIGINS=https://mentepausada.com,https://app.mentepausada.com
```

---

## 🚀 Próximos Pasos

1. **Ahora:** Confirmar flujos de datos (¿dónde se registran compras reales?)
2. **Semana 1:** Integrar SendGrid para emails
3. **Semana 2:** Configurar webhooks de Stripe en producción
4. **Semana 3:** Activar ads (Meta + Google) con copy variants
5. **Semana 4:** Lanzar Polt content automation
6. **Semana 5:** Validar primeras 3 ideas de Cerebro

---

*Actualizado: 2026-04-17*
