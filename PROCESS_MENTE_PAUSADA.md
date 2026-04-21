# Mente Pausada - Flujo Detallado de Automatización

## 📋 Resumen Ejecutivo

Mente Pausada es un **producto digital one-time**: ebook + 25 audios de meditación/mindfulness.

- **Público:** Profesionales 25-45, bienestar, LATAM (Argentina especialmente)
- **Precios:** $99 (Premium), $149 (Premium Plus), $199 (Premium VIP)
- **Modelo:** Venta directa + email secuencias + upsells
- **Objetivo:** $5,000/mes en ingresos

---

## 🔄 Flujo Completo del Cliente

### Fase 1: Generador de Leads (Publicidad)

**Canales:** Meta (Facebook/Instagram) + Google Ads

**Copys Generados (Skill: ads-mente-pausada)**
- Variante 1: Emocional ("Calmate en 1 minuto")
- Variante 2: Racional ("Método probado: 4-7-8 breathing")
- Variante 3: Urgencia ("14 personas compraron hoy")
- Variante 4: Social Proof (testimonios)
- Variante 5: Aspirational ("La calma que buscabas")

**Presupuesto:** $20-50/día flexible
- Meta 70% ($14-35/día) → profesionales + bienestar
- Google 30% ($6-15/día) → keywords intención de compra

**Objetivo:** 0.5-2% CTR, <$3 CPC, >8% conversion rate

---

### Fase 2: Landing Page → Compra

**Landing Page Components**
1. **Hero Section**
   - Headline: "Calma en 1 minuto. Para mentes aceleradas."
   - Subheadline: "Método comprobado de mindfulness + 25 audios"
   - CTA: "Acceder ahora" (botón verde prominente)

2. **Problem Section**
   - Mostrar estrés/ansiedad = problema real
   - Pain point específico

3. **Solution Section**
   - Qué es Mente Pausada
   - Cómo funciona (4-7-8 breathing explicado)
   - Por qué funciona (base científica)

4. **Social Proof**
   - 3-5 testimonios con nombre, foto, métricas
   - "Ha ayudado a 2,500+ personas"
   - Ratings/scores

5. **Pricing Section**
```
┌─────────────┬──────────────┬─────────────┐
│  PREMIUM    │ PREMIUM PLUS │ PREMIUM VIP │
│    $99      │     $149     │    $199     │
├─────────────┼──────────────┼─────────────┤
│ • Ebook     │ • Ebook      │ • Ebook     │
│ • 25 audios │ • 25 audios  │ • 25 audios │
│             │ • Templates  │ • Templates │
│             │ • Worksheets │ • Worksheets│
│             │              │ • 6 mo     │
│             │              │   community │
└─────────────┴──────────────┴─────────────┘
```

6. **FAQ**
   - ¿Cuánto tiempo toman los audios?
   - ¿Garantía de satisfacción?
   - ¿Acceso de por vida?

7. **CTA Final**
   - Botón destacado "Comprar ahora"
   - Risk reversal: "30-day money-back guarantee"

**Checkout Flow (Stripe)**
```
Cliente cliquea "Comprar ahora"
  ↓
Selecciona tier (Premium/Plus/VIP)
  ↓
Ingresa email
  ↓
Redirige a Stripe Checkout
  ↓
Stripe gestiona pago (tarjeta, Apple Pay, etc)
  ↓
Pago exitoso → Stripe webhook
  ↓
Nuestro backend:
  ├─ Crea record Purchase
  ├─ Genera access_token
  ├─ Envía email day_0
  └─ Redirige a página de descarga
```

---

### Fase 3: Email Sequence (5 Emails en 14 días)

**Tecnología:** SendGrid + scheduled task (4x diarios)

**Timeline Automatizado:**

#### Email 1: Day 0 (5 minutos después de compra)
**Subject:** ¡Bienvenido a Mente Pausada! 🧘 Acceso inmediato
**Propósito:** Entrega + instrucciones

```
Hola {name},

¡Gracias por confiar en Mente Pausada!

Tu compra fue exitosa. Aquí está tu acceso:

📥 Descarga el ebook: [DOWNLOAD_LINK_EXPIRES_30_DAYS]
🎵 Accede a los audios: [AUDIO_LINK]
👥 Comunidad privada: [COMMUNITY_LINK] (si VIP)

EMPIEZA HOY: Elige el audio de 1 minuto que más te llame la atención.
No necesitas preparación, solo elige y respira.

Preguntas: Responde a este email.

Con calma,
Mente Pausada
```

#### Email 2: Day 3 (72 horas después)
**Subject:** La magia empieza hoy 🎵 Tu primer audio
**Propósito:** Educación + motivación

```
Hola {name},

Es hora de que experimentes qué hace especial a Mente Pausada.

El audio de HOY (1 minuto) te va a mostrar algo que probablemente no esperabas:
que PUEDES cambiar tu estado emocional en menos del tiempo que tardas en hacer café.

🎯 Método que enseño: La respiración de 4-7-8
Resultado: Bajás cortisol en segundos.

👉 [LISTEN NOW BUTTON]

Mañana vamos con otro. Sin prisa. A tu ritmo.

Con calma,
Mente Pausada
```

#### Email 3: Day 7 (168 horas)
**Subject:** Esto es lo que otros están logrando 💭
**Propósito:** Social proof + comunidad

```
Hola {name},

Quería compartirte algo que sucedió en nuestra comunidad esta semana:

"No me imaginaba que en 1 minuto pudiera cambiar mi respiración. Increíble." — María, 32
"Por fin pude parar antes de explotar. Gracias." — Juan, 38
"Los audios son cortos pero efectivos. Es lo que buscaba." — Ana, 28

¿Cuál es TU experiencia hasta ahora?

Responde a este email. Me encanta saber cómo va.

Con calma,
Mente Pausada
```

#### Email 4: Day 10 (240 horas)
**Subject:** Escalá tu práctica 🚀 (Opcional)
**Propósito:** Upsell a servicios premium

```
Hola {name},

Si te gustó Mente Pausada, aquí hay opciones para profundizar:

1️⃣ **Coaching 1-on-1 ($500)**
   - Sesión de 60 min personalizada
   - Diseñamos tu práctica según TU vida

2️⃣ **Comunidad Premium ($99/mes)**
   - Acceso a sesiones en vivo
   - Contenido exclusivo
   - Grupo privado de apoyo

Pero sin presión. El ebook + audios que compraste valen cada centavo.

Si el 1-on-1 te interesa, responde "coaching" a este email.

Con calma,
Mente Pausada
```

#### Email 5: Day 14 (336 horas)
**Subject:** Cuéntame: ¿Cómo va la experiencia?
**Propósito:** Feedback + reenganche

```
Hola {name},

Hace 2 semanas que compraste Mente Pausada.

Me gustaría saber:
- ¿Cuál audio es tu favorito?
- ¿Notaste cambios en tu calma/estrés?
- ¿Qué te gustaría mejorar?

Esta retroalimentación nos ayuda a hacer Mente Pausada mejor para ti.

Responde aquí. Tu opinión importa.

Con calma,
Mente Pausada

P.S. Si no abriste los audios aún, empieza hoy. 1 minuto. Eso es todo.
```

**Scheduling Logic**
```python
current_time = datetime.now()
days_since_purchase = (current_time - purchase.created_at).days

if days_since_purchase == 0:
    email_to_send = "day_0"
elif days_since_purchase == 3:
    email_to_send = "day_3"
elif days_since_purchase == 7:
    email_to_send = "day_7"
elif days_since_purchase == 10:
    email_to_send = "day_10"
elif days_since_purchase == 14:
    email_to_send = "day_14"

if email_to_send and not already_sent:
    send_via_sendgrid(purchase.email, template=EMAIL_TEMPLATES[email_to_send])
    purchase.email_sequence_status = email_to_send
    purchase.email_sent_count += 1
```

---

### Fase 4: Analytics & Optimization (5 PM Diariamente)

**Tarea:** `daily-analytics-mente-pausada` (5 PM Argentina time)

**Métricas Calculadas:**

| Métrica | Hoy | 7 días | 30 días | Meta |
|---------|-----|--------|---------|------|
| Compras | X | X | X | X/día |
| Revenue | $X | $X | $X | $5000 |
| AOV | $X | $X | $X | $150+ |
| Conv% | X% | X% | X% | >8% |
| ROAS | X.Xx | X.Xx | X.Xx | >2x |

**Análisis Incluye:**
1. Revenue diario y acumulado
2. Conversión rate (últimos 7d)
3. Breakdown por tier (Basic/Plus/VIP %)
4. ROAS por canal (Meta vs Google)
5. Email open rates (si disponible)
6. Trending (comparar con semana anterior)
7. Recomendaciones automáticas

**Recomendaciones Automáticas:**
```
IF ROAS > 3.0:
  "Duplica presupuesto en próximos 3 días"

IF ROAS between 1.5-3.0:
  "Mantén presupuesto, A/B test copies"

IF ROAS < 1.5:
  "Pausa ads, analiza targeting o landing page"

IF conversion_rate < 5%:
  "A/B test headlines o proposición de valor"

IF VIP > 40% of sales:
  "Promover más el tier VIP"

IF email_open_rate > 30%:
  "Crear más contenido similar"
```

---

## 🛠️ Integración Técnica

### Base de Datos (Schema)
```sql
CREATE TABLE purchases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  product_tier VARCHAR(20) NOT NULL,  -- basic/plus/vip
  amount DECIMAL(10,2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'USD',
  payment_status VARCHAR(20) DEFAULT 'pending',  -- success/failed
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  
  -- Email sequence
  email_sequence_status VARCHAR(20),
  last_email_sent_at DATETIME,
  email_sent_count INTEGER DEFAULT 0,
  
  -- Analytics
  utm_source VARCHAR(100),
  utm_campaign VARCHAR(100),
  ip_address VARCHAR(45),
  
  -- Access
  access_token VARCHAR(255),
  access_expires_at DATETIME DEFAULT (datetime('now', '+30 days'))
);

CREATE INDEX idx_email ON purchases(email);
CREATE INDEX idx_created_at ON purchases(created_at);
```

### API Endpoints

**Checkout**
```
POST /api/checkout/create-session
Input: {
  product_tier: "basic|plus|vip",
  email: "user@example.com",
  utm_source: "meta|google|organic"
}
Output: {
  checkout_url: "https://checkout.stripe.com/pay/...",
  session_id: "cs_live_..."
}
```

**Webhook (Stripe)**
```
POST /api/webhook/stripe
Event: payment_intent.succeeded
Action:
  1. Crea Purchase record
  2. Envía email day_0
  3. Genera access_token
  4. Retorna download link
```

**Analytics**
```
GET /api/analytics/mente-pausada?range=7d
Output: {
  today: {
    purchases: X,
    revenue: $X,
    conversion_rate: X%
  },
  seven_days: { ... },
  thirty_days: { ... },
  by_tier: {
    basic: { purchases: X, revenue: $X },
    plus: { purchases: X, revenue: $X },
    vip: { purchases: X, revenue: $X }
  },
  by_channel: {
    meta: { conversions: X, spend: $X, roas: X.Xx },
    google: { ... }
  }
}
```

---

## 🎯 Key Metrics to Monitor

1. **Conversion Rate:** Target >8%
   - Landing page → Compra
   - A/B test headlines, testimonios, CTA placement

2. **AOV (Average Order Value):** Target $150+
   - Cuál tier más vendido
   - Si VIP >40%: promover más

3. **ROAS (Return on Ad Spend):** Target >2x
   - Meta ROAS vs Google ROAS
   - Copy variant performance
   - Audience performance

4. **CAC (Cost per Acquisition):** Target <$30
   - Ad spend / conversiones
   - Optimizar targeting

5. **Email Metrics**
   - Open rate: Target >30%
   - Click rate: Target >5%
   - Response rate (coaching offers)

---

## ⚠️ Problemas Comunes & Soluciones

| Problema | Solución |
|----------|----------|
| Conversion <5% | A/B test testimonios, CTA, precio |
| AOV bajo (gente elige Basic) | Fortalecer propuesta Plus/VIP |
| ROAS <1.5 | Cambiar targeting, copy variants, landing page |
| Email opens bajos | Cambiar subject line, A/B test |
| Alto bounce rate | Verificar mobile design, velocidad |

---

## 📅 Roadmap (Próximas 4 semanas)

- **Semana 1:** Landing live + Stripe testing
- **Semana 2:** Ads activos (Meta + Google), email sequences
- **Semana 3:** A/B test copies basado en performance
- **Semana 4:** Optimizaciones finales, análisis ROI

---

*Actualizado: 2026-04-17*
