# ⚙️ Integración Técnica - Checklist Detallado

**Estado:** Fase 2 estructura completa, pero APIs NO están vivas  
**Criticidad:** 🔴 ALTO - APIs necesitan implementación real

---

## 🔴 CRÍTICO (Bloquea funcionamiento)

### 1. Email Sending NOT IMPLEMENTED
**Estado:** 🔴 BLOCKER  
**Archivo:** `backend/app/email_sequences.py` líneas 166-180  
**Problema:** Código está commented-out (SMTP placeholder)

```python
# TODO: ACTUAL CODE NEEDED HERE
# Currently this is just a placeholder
# server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
# server.login(SENDER_EMAIL, SENDER_PASSWORD)
```

**Qué falta:**
1. Implementar función `send_email_sendgrid()` usando SendGrid API
2. Importar: `from sendgrid import SendGridAPIClient`
3. Crear email object con templates
4. Error handling y retries
5. Logging de enviados/fallidos

**Tiempo estimado:** 2-3 horas  
**Prioridad:** 🔴 MÁXIMA

---

### 2. Stripe Webhook NO Testado
**Estado:** 🟡 PARCIAL  
**Archivo:** `backend/app/api/checkout.py` líneas 30-50  
**Problema:** Estructura está lista pero:
- No hay error handling si falla creación de Purchase
- No hay verificación de webhook signature
- No hay idempotencia (¿si webhook llega 2x?)

**Qué falta:**
```python
# Verificar firma del webhook
from stripe.error import SignatureVerificationError

try:
    event = stripe.Webhook.construct_event(
        body, sig_header, endpoint_secret
    )
except SignatureVerificationError:
    # Return error response
    pass
```

**Tiempo estimado:** 1-2 horas  
**Prioridad:** 🔴 MÁXIMA

---

### 3. Database Schema NOT Created
**Estado:** 🔴 BLOCKER  
**Problema:** Models definidos pero schema SQL NO existe en BD

**Qué falta:**
1. Crear migrations (usando Alembic o directas)
2. Ejecutar CREATE TABLE statements
3. Verificar índices están creados
4. Test de conexión a BD

**Archivos afectados:**
```
backend/app/models/purchase.py
backend/app/models/order.py
backend/app/models/idea.py
```

**SQL a ejecutar:**
```sql
-- En backend/alembic/versions/ crear migration
-- O ejecutar directo en sqlite:
CREATE TABLE purchases ( ... )
CREATE TABLE orders ( ... )
CREATE TABLE ideas ( ... )
```

**Tiempo estimado:** 1 hora  
**Prioridad:** 🔴 MÁXIMA

---

### 4. API Routes NOT Registered
**Estado:** 🔴 BLOCKER  
**Archivo:** `backend/app/main.py`  
**Problema:** Routes creadas pero NO importadas/registradas

**Qué falta:**
```python
from app.api import purchases, orders, ideas, checkout

app.include_router(purchases.router, prefix="/api/purchases", tags=["purchases"])
app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])
app.include_router(checkout.router, prefix="/api/checkout", tags=["checkout"])
```

**Verificar:**
- [ ] main.py tiene imports correctos
- [ ] Router decorators tienen @router.get/post/put/delete
- [ ] Prefixes son correctos
- [ ] Test que endpoints responden: `curl http://localhost:8000/api/purchases`

**Tiempo estimado:** 30 minutos  
**Prioridad:** 🔴 MÁXIMA

---

## 🟠 ALTO (Necesario antes de producción)

### 5. Input Validation Missing
**Estado:** 🟠 IMPORTANTE  
**Problema:** Endpoints aceptan cualquier input sin validar

**Qué falta:**
```python
from pydantic import BaseModel, EmailStr, validator

class PurchaseCreate(BaseModel):
    email: EmailStr  # Valida que sea email válido
    product_tier: str
    
    @validator('product_tier')
    def tier_valid(cls, v):
        if v not in ['basic', 'plus', 'vip']:
            raise ValueError('Invalid tier')
        return v

@router.post("/")
async def create_purchase(purchase: PurchaseCreate):
    # Pydantic automáticamente valida
    pass
```

**Ubicación:** Todos los endpoints en `api/`  
**Tiempo estimado:** 2 horas  
**Prioridad:** 🟠 ALTO

---

### 6. Error Handling Missing
**Estado:** 🟠 IMPORTANTE  
**Problema:** Sin try/except ni response codes coherentes

**Qué falta:**
```python
@router.get("/{purchase_id}")
async def get_purchase(purchase_id: int, db: AsyncSession):
    try:
        purchase = await db.get(Purchase, purchase_id)
        if not purchase:
            raise HTTPException(status_code=404, detail="Purchase not found")
        return purchase
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal error")
```

**Ubicación:** Todos los endpoints  
**Tiempo estimado:** 2 horas  
**Prioridad:** 🟠 ALTO

---

### 7. Authentication Missing
**Estado:** 🟠 IMPORTANTE  
**Problema:** Endpoints públicos, sin protección

**Qué falta:**
- Si admin dashboard: requiere login
- Si cliente: requiere API key o JWT token
- Decisión: ¿Open API o private?

**Recomendación:** `GET /api/analytics` requiere admin token, pero `POST /api/checkout` es público

**Tiempo estimado:** 2-3 horas  
**Prioridad:** 🟠 MEDIO-ALTO

---

### 8. Tests Missing
**Estado:** 🟠 IMPORTANTE  
**Problema:** Cero tests para APIs

**Qué falta:**
```python
# backend/tests/test_purchases.py
import pytest
from app.api.purchases import router

@pytest.mark.asyncio
async def test_create_purchase(client):
    response = await client.post("/api/purchases", json={
        "email": "test@example.com",
        "product_tier": "basic",
        "amount": 99.00
    })
    assert response.status_code == 201
    assert response.json()["id"]
```

**Mínimo necesario:**
- test_purchases.py (CRUD operations)
- test_checkout.py (Stripe integration)
- test_email_sequences.py (Email sending)

**Tiempo estimado:** 4 horas  
**Prioridad:** 🟠 MEDIO

---

## 🟡 MEDIO (Nice to have pero no bloquea)

### 9. Logging Not Configured
**Estado:** 🟡 MEDIO  
**Problema:** Sin logging centralizado

**Qué falta:**
```python
import logging

logger = logging.getLogger(__name__)

# Setup en main.py
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/logs/app.log'),
        logging.StreamHandler()
    ]
)
```

**Tiempo estimado:** 1 hora  
**Prioridad:** 🟡 BAJO-MEDIO

---

### 10. Rate Limiting Missing
**Estado:** 🟡 MEDIO  
**Problema:** Sin protección contra spam/abuse

**Qué falta:**
```python
from slowapi import Limiter

limiter = Limiter(key_func=get_remote_address)

@app.get("/api/purchases")
@limiter.limit("100/minute")
async def get_purchases():
    pass
```

**Ubicación:** Endpoints sensibles (checkout, orders)  
**Tiempo estimado:** 1 hora  
**Prioridad:** 🟡 BAJO-MEDIO

---

### 11. Logging/Monitoring Dashboard
**Estado:** 🟡 MEDIO  
**Problema:** Sin visibilidad de errores en tiempo real

**Qué falta:**
- Sentry integration (error tracking)
- DataDog/New Relic (performance monitoring)
- O al menos file-based logs que se revisen

**Tiempo estimado:** 2-3 horas  
**Prioridad:** 🟡 BAJO

---

## 📋 SKILLS A CREAR (Solicitados por usuario)

### 12. /humanizer Skill
**Estado:** 🔴 NOT CREATED  
**Requisito:** User pidió explícitamente

```markdown
---
name: humanizer
description: Make AI output sound natural and human-written
---

Take any AI-generated text and make it:
- Sound conversational (less formal)
- Add natural hesitations/informal language
- Include personality and humor where appropriate
- Break up long paragraphs
- Use contractions naturally
```

**Tiempo:** 30 minutos  
**Prioridad:** 🟠 ALTO

---

### 13. /concise Skill  
**Estado:** 🔴 NOT CREATED  
**Requisito:** User pidió explícitamente

```markdown
---
name: concise
description: Provide direct answers without introductions
---

Rules:
1. No opening phrases ("Let me...", "I'll...", "So...")
2. No summaries at end
3. One sentence context if needed, then answer
4. Code first if code task
5. Lists/bullets for clarity
6. No "here's what we did" - just what was done
```

**Tiempo:** 30 minutos  
**Prioridad:** 🟠 ALTO

---

## 🔧 Implementation Priority Order

**Orden recomendado para hacer funcionarm todo:**

```
SEMANA 1 (Make It Work)
├─ Día 1-2: Stripe webhook + error handling
├─ Día 3: SendGrid email integration  
├─ Día 4: Database schema creation
├─ Día 5: Register API routes en main.py
└─ Día 5 EOD: Test full flow: landing → pago → email

SEMANA 2 (Make It Robust)
├─ Input validation en todos endpoints
├─ Error handling y proper HTTP codes
├─ Basic auth (si necesario)
├─ Create /humanizer skill
├─ Create /concise skill
└─ Deploy frontend landing

SEMANA 3 (Make It Observable)
├─ Setup logging
├─ Add basic tests (purchases, checkout)
├─ Rate limiting en endpoints sensibles
├─ Monitoring setup (Sentry o similar)
└─ Ready para ads/traffic real
```

---

## ✅ Implementation Checklist

### Antes de activar en vivo:

**Mente Pausada - Landing + Pago:**
- [ ] SendGrid email sending working
- [ ] Stripe webhook verified
- [ ] Database schema created
- [ ] API routes registered
- [ ] Landing page deployed
- [ ] Test compra end-to-end funciona
- [ ] Email day_0 llega en inbox
- [ ] Analytics dashboard muestra compra
- [ ] /humanizer skill creado
- [ ] /concise skill creado

**Polt Mobilier - Content + Orders:**
- [ ] Content generation tarea lista
- [ ] Order creation skill en progreso
- [ ] Email notificaciones por hito
- [ ] Production dashboard working

**Cerebro - Ideas:**
- [ ] Idea generation skill en progreso
- [ ] Market validation skill en progreso

---

## 📞 If You Get Stuck...

**"SendGrid email no se envía"**
→ Verificar: API key en .env, sender_email correcto, firewall/blocklist

**"Stripe webhook no recibe eventos"**
→ Verificar: webhook endpoint registrado en Stripe dashboard, IP whitelisted, endpoint_secret en .env

**"POST /api/purchases retorna error"**
→ Verificar: schema de Purchase table existe, email es único, pydantic models importados

**"Scheduled tasks no corren"**
→ Verificar: SKILL.md está en .claude/scheduled-tasks/, cron expression válida

**"Landing page no carga"**
→ Verificar: deployed en Netlify/Vercel, CORS configurado en backend

---

## 🎯 Success Criteria

Sistema está **LISTO PARA PRODUCCIÓN** cuando:

- ✅ Landing page activa recibe traffic
- ✅ Compra registra en BD sin errores
- ✅ Email day_0 enviado automáticamente
- ✅ Analytics dashboard muestra métricas reales
- ✅ Scheduled tasks corren diariamente sin error
- ✅ ROAS calculado correctamente
- ✅ Stripe webhook recibe pagos
- ✅ Zero 500 errors en logs

**Meta:** Alcanzar esto en 2 semanas

---

*Última actualización: 2026-04-17*  
*Crítico: Iniciar por items 🔴 CRÍTICO*
