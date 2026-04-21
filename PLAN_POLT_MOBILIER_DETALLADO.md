# 🛋️ PLAN POLT MOBILIER - ANÁLISIS DETALLADO

**Objetivo:** Automatizar flujo de órdenes (lead → orden → producción → entrega)  
**Modelo:** Consulta → Presupuesto → Orden → Tracking → Entrega → Feedback  
**Timeline:** 2 sesiones (4-6 horas) = FULL AUTOMATION

---

## ✅ QUÉ TIENE (50% hecho)

### 1. BRAND PROFILE COMPLETO ✅

**Ubicación:** `backend/app/brands/polt_mobilier.py`

```python
brand = {
    "name": "Polt Mobilier",
    "type": "Custom furniture",
    "audience": "Arquitectos, diseñadores, propietarios",
    "specialty": "Muebles personalizados, alta calidad",
    "pricing_model": "Por proyecto (variable $500-5k)",
    "production_time": "2-4 semanas",
    "channels": ["Instagram", "WhatsApp", "Email"]
}
```

**Status:** ✅ Perfil claro

---

### 2. CALCULATOR FUNCIONAL EN NETLIFY ✅

**Ubicación:** `https://incredible-tapioca-c3c3f1.netlify.app/` (YA EN VIVO)

**Lo que hace:**
```
✅ Cliente selecciona dimensiones
✅ Elige material (madera, tela, etc)
✅ Calcula precio automático
✅ Captura email
✅ Envía presupuesto por email (MANUAL aún)
```

**Archivos relacionados:**
```
archived-assets/polt-dashboards/
├── polt_calculator.html
├── polt_calculator_pro.html
├── polt_dashboard_v5_with_analyzer.html  ← MEJOR VERSIÓN
```

**Status:** ✅ Calculator funciona, pero solo en HTML (no conectada a BD)

---

### 3. PERFILES DE USUARIO DEFINIDOS ✅

```
PERFIL 1: Cliente Potencial
├─ Acceso: Landing + Calculator
├─ Acción: Calcula presupuesto + deja email
└─ Estado: Lead en BD

PERFIL 2: Carpintero/Productor
├─ Acceso: Dashboard de órdenes en progreso
├─ Acción: Ve órdenes, actualiza status, sube fotos
└─ Estado: Notificado de cada hito

PERFIL 3: Admin (Tú)
├─ Acceso: Dashboard completo + analytics
├─ Acción: Aprueba órdenes, ve ingresos, métricas
└─ Estado: Reporte diario 5 PM
```

**Status:** ✅ Perfiles claros

---

### 4. DATABASE MODELS DEFINIDOS ✅

**Ubicación:** `backend/app/models/`

**Order Model:**
```python
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    
    # Cliente
    customer_email = Column(String(200))
    customer_name = Column(String(100))
    customer_phone = Column(String(20))
    
    # Proyecto
    project_name = Column(String(200))
    description = Column(Text)
    
    # Dimensiones
    width = Column(Float)  # cm
    height = Column(Float)  # cm
    depth = Column(Float)  # cm
    
    # Material & Acabado
    material = Column(String(100))  # madera, tela, etc
    finish = Column(String(100))  # color, barniz
    
    # Precio & Pago
    estimated_price = Column(Float)
    final_price = Column(Float)
    currency = Column(String(10), default="USD")
    status = Column(String(50))  # pending, confirmed, in_production, ready, delivered
    
    # Tracking
    start_date = Column(DateTime)
    estimated_end_date = Column(DateTime)
    actual_end_date = Column(DateTime)
    
    # Notas
    notes = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

**Status:** ✅ Modelo completo

---

### 5. API ROUTES BÁSICAS DEFINIDAS ✅

**Ubicación:** `backend/app/api/orders.py`

```python
@router.get("/orders")  # Lista todas órdenes
@router.post("/orders")  # Crea nueva orden
@router.get("/orders/{id}")  # Obtiene orden por ID
@router.put("/orders/{id}")  # Actualiza orden
@router.delete("/orders/{id}")  # Cancela orden
```

**Status:** ✅ Endpoints existen, pero sin lógica de negocio

---

### 6. BACKEND API REGISTRADA ✅

**Ubicación:** `backend/app/main.py` línea 49

```python
app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
```

**Status:** ✅ Router registrado

---

### 7. DOCUMENTACIÓN DE PROCESO ✅

**Ubicación:** `PROCESS_POLT_MOBILIER.md`

```
Contiene:
✅ Flujo completo lead → orden → producción
✅ Email templates por hito
✅ Métricas a trackear
✅ Timeline de producción típico
```

**Status:** ✅ Documentación excelente

---

## 🔴 QUÉ FALTA (50% - 6 cosas importantes)

### 1. 🔴 SKILL "GESTOR-ORDENES-POLT" (IMPORTANTE)

**Qué es:**
Agente que:
- ✅ Recibe: presupuesto del cliente + confirmación
- ✅ Genera: orden interna
- ✅ Crea: guía de trabajo para carpintero
- ✅ Notifica: a cliente + carpintero

**Ubicación:** Debe crearse en `backend/app/agents/gestor_ordenes_polt.py`

**Pseudocódigo necesario:**
```python
class OrderManagerAgent:
    
    async def create_order(self, email: str, presupuesto_dict: dict):
        """
        Input: {
            "email": "cliente@example.com",
            "customer_name": "Juan Pérez",
            "width": 150,
            "height": 80,
            "depth": 40,
            "material": "madera", 
            "finish": "nogal",
            "estimated_price": 1500
        }
        """
        
        # 1. Validar que no exista orden similar
        existing = await db.query(Order).filter(
            Order.customer_email == email,
            Order.status.in_(["pending", "confirmed"])
        ).first()
        
        # 2. Crear orden en BD
        order = Order(
            customer_email=email,
            customer_name=presupuesto_dict["customer_name"],
            width=presupuesto_dict["width"],
            # ... etc
            status="pending",
            start_date=datetime.now()
        )
        await db.add(order)
        await db.commit()
        
        # 3. Generar guía de trabajo para carpintero
        guide = generate_work_guide(order)
        
        # 4. Notificar cliente
        await send_email_order_confirmation(email, order)
        
        # 5. Notificar carpintero
        await send_email_carpenter_new_order(order)
        
        return {"order_id": order.id, "status": "created"}
    
    async def update_order_status(self, order_id: int, new_status: str, notes: str = ""):
        """
        Estados permitidos:
        pending → confirmed → in_production → ready → delivered
        """
        order = await db.get(Order, order_id)
        order.status = new_status
        order.notes = notes
        await db.commit()
        
        # Notificar cliente del cambio
        await send_email_order_status_update(order.customer_email, order, new_status)
        
        return {"status": "updated"}
    
    async def upload_progress_photo(self, order_id: int, photo_url: str):
        """
        Carpintero sube foto del progreso
        """
        order = await db.get(Order, order_id)
        order.progress_photos.append(photo_url)
        await db.commit()
        
        # Notificar cliente
        await send_email_progress_photo(order.customer_email, order)
        
        return {"photo_added": True}
```

**Skill como SKILL.md:**

La idea es tener un skill `/gestor-ordenes-polt` que:
- Lee presupuesto aprobado por cliente
- Transforma en orden formal
- Genera workflows para carpintero
- Dispara notificaciones

**Tiempo:** 2-3 horas

**Impacto:** IMPORTANTE - Sin esto, no hay seguimiento de órdenes

---

### 2. 🔴 EMAIL AUTOMÁTICO POR HITO (IMPORTANTE)

**Ubicación:** Crear `backend/app/email_polt_notifications.py`

**5 Emails a implementar:**

```
EMAIL 1: CONFIRMACIÓN ORDEN (Inmediato)
├─ Subject: "Tu orden Polt está confirmada ✅"
├─ To: cliente@example.com
├─ Body: 
│   - Resumen: dimensiones, material, precio
│   - Fecha estimada de entrega
│   - Próximos pasos
│   - Link para ver estado en dashboard
└─ When: Cuando status = "confirmed"

EMAIL 2: PRODUCCIÓN INICIADA (Día 1)
├─ Subject: "Tu mueble entró en producción 🔨"
├─ To: cliente@example.com
├─ Body:
│   - "El carpintero comenzó a trabajar"
│   - "Fecha estimada: 2 semanas"
│   - "Te mostraremos fotos del progreso"
└─ When: Cuando status = "in_production"

EMAIL 3: FOTO DE PROGRESO (Día 7)
├─ Subject: "¡Mira cómo va tu mueble! 📸"
├─ To: cliente@example.com
├─ Body:
│   - Foto del mueble en construcción
│   - "Ya está casi listo"
│   - "Una semana más"
└─ When: Cuando carpenter sube foto

EMAIL 4: LISTO PARA ENTREGA (Día 14)
├─ Subject: "Tu mueble está listo 🎉"
├─ To: cliente@example.com
├─ Body:
│   - "Tu mueble está en almacén"
│   - "Coordina entrega aquí [LINK CALENDLY]"
│   - "Forma de pago final"
└─ When: Cuando status = "ready"

EMAIL 5: ENTREGADO + FEEDBACK (Post-entrega)
├─ Subject: "Entrega completada ✨"
├─ To: cliente@example.com
├─ Body:
│   - "Gracias por confiar en Polt"
│   - "¿Te encantó tu mueble? [LINK FEEDBACK]"
│   - "Recomendaciones de mantenimiento"
│   - Upsell: "Restauración, reparaciones, nuevos proyectos"
└─ When: Cuando status = "delivered"
```

**Código necesario:**
```python
async def send_order_email_by_status(order_id: int, status: str):
    """
    Dispara email automático según status de orden
    """
    order = await db.get(Order, order_id)
    
    templates = {
        "confirmed": EMAIL_TEMPLATES["order_confirmed"],
        "in_production": EMAIL_TEMPLATES["production_started"],
        "ready": EMAIL_TEMPLATES["ready_for_delivery"],
        "delivered": EMAIL_TEMPLATES["delivery_complete"]
    }
    
    template = templates.get(status)
    if template:
        await send_email_sendgrid(
            to_email=order.customer_email,
            subject=template["subject"],
            body=template["body"].format(
                name=order.customer_name,
                product=order.project_name,
                date=order.estimated_end_date
            )
        )
```

**Tiempo:** 1-2 horas

**Impacto:** IMPORTANTE - Sin esto, cliente no sabe qué pasa con su orden

---

### 3. 🔴 DASHBOARD CONECTADO A BD (IMPORTANTE)

**Ubicación:** Convertir HTML v5 a React + conectar a BD

**Actualmente:**
- ✅ HTML dashboard v5 existe
- ❌ Solo muestra datos fake/hardcoded
- ❌ No conectado a BD

**Qué hacer:**

```
Opción A: Convertir HTML → React
├─ Recrear v5 como componente React
├─ Conectar a API /api/v1/orders
├─ Agregar real-time updates
└─ Time: 2-3 horas

Opción B: Usar HTML actual + API
├─ Dejar HTML v5 como está
├─ Agregar JavaScript para fetch /api/v1/orders
├─ Auto-refresh cada 1 minuto
└─ Time: 1-2 horas (más rápido)
```

**Funcionalidades necesarias:**

```
✅ Listar todas órdenes activas
├─ Columnas: Cliente, Proyecto, Status, Fecha inicio, Estimado
├─ Filtros: Por status, por fecha, por cliente
└─ Búsqueda: Por nombre cliente o proyecto

✅ Vista detalle de orden
├─ Mostrar: Dimensiones, material, precio, notas
├─ Foto progreso: Subir + mostrar
├─ Cambiar status: Buttons para cada transición
└─ Histórico: Qué cambió y cuándo

✅ Analytics
├─ Órdenes activas HOY
├─ Órdenes completadas MES
├─ Revenue total mes
├─ Tiempo promedio producción
├─ Satisfacción cliente (si hay data)

✅ Para Carpenter
├─ Ver SOLO sus órdenes
├─ Botones: "En progreso", "Listo", "Entregado"
├─ Subir fotos
└─ Chat/notas con cliente (opcional)

✅ Para Admin (Tú)
├─ Ver TODO
├─ Analytics completo
├─ Exportar órdenes a PDF/Excel
└─ Reportes por carpintero (productividad)
```

**Tiempo:** 2-3 horas

**Impacto:** IMPORTANTE - Sin esto, no hay visibilidad en tiempo real

---

### 4. 🔴 CONTENIDO AUTOMATIZADO 9 AM (IMPORTANTE)

**Qué es:**
Tarea diaria que genera contenido para Instagram + email

**Ubicación:** Crear `backend/app/tasks/daily_content_polt.py`

**Qué genera:**
```
Cada día a las 9 AM:
├─ 1 Instagram carousel (proyecto + before-after)
│  ├─ Slide 1: Portada "Nuevo proyecto Polt"
│  ├─ Slide 2-4: Fotos del proyecto
│  ├─ Slide 5: Precio + contacto
│  └─ Caption: Copy persuasivo + CTA
│
├─ 1 Instagram reel (30s) - Timelapse de producción
│  └─ O mostrar antes/después rápido
│
└─ 1 Email newsletter
   ├─ Asunto: "[Esta semana] Proyectos nuevos Polt"
   ├─ Body: 3-5 últimos proyectos entregados
   └─ CTA: "Solicita tu presupuesto"
```

**Código necesario:**

```python
async def daily_content_polt_task():
    """Tarea 9 AM cada día"""
    
    # 1. OBTENER ÚLTIMOS PROYECTOS COMPLETADOS
    completed_projects = await db.query(Order).filter(
        Order.status == "delivered",
        Order.updated_at >= datetime.now() - timedelta(days=30)
    ).order_by(Order.updated_at.desc()).limit(5)
    
    # 2. GENERAR CAROUSEL INSTAGRAM
    carousel = generate_instagram_carousel(completed_projects[0])
    # Retorna: {
    #   "images": [url1, url2, url3, url4, url5],
    #   "caption": "Copy generado por IA",
    #   "hashtags": "#polt #muebles #carpinteria #diseño"
    # }
    
    # 3. SUBIR A INSTAGRAM (via API)
    await post_to_instagram(carousel)
    
    # 4. GENERAR REEL
    reel = generate_timelapse_reel(completed_projects[0])
    await post_to_instagram_reel(reel)
    
    # 5. ENVIAR EMAIL NEWSLETTER
    newsletter = generate_newsletter(completed_projects)
    await send_newsletter_email(
        to_list=get_email_subscribers(),
        subject="Nuevos proyectos Polt esta semana",
        body=newsletter
    )
    
    # 6. GUARDAR EN BD
    await db.create(ContentLog, {
        "date": datetime.now(),
        "type": "carousel",
        "status": "published",
        "engagement": 0  # se actualiza después
    })
```

**Requisitos:**
```
✅ Conexión Instagram Graph API (para subir posts)
✅ Buffer API (alternativa: agendar posts)
✅ IA para copywriting (prompt a Claude)
✅ Librería imagen (PIL para crear carousel)
✅ SendGrid para newsletter
```

**Tiempo:** 2-3 horas

**Impacto:** IMPORTANTE - Sin esto, marketing es manual

---

### 5. 🟠 VALIDACIÓN & ERROR HANDLING (IMPORTANTE)

**Ubicación:** `backend/app/api/orders.py`

**Qué falta:**
```python
# AHORA: Sin validación
@router.post("/orders")
async def create_order(order_data: dict):
    # Acepta cualquier cosa
    order = Order(**order_data)
    
# DEBE SER: Con validación
from pydantic import BaseModel, validator

class OrderCreate(BaseModel):
    customer_email: str  # Email válido
    customer_name: str  # No vacío
    width: float  # Debe ser > 0
    height: float  # Debe ser > 0
    depth: float  # Debe ser > 0
    material: str  # Debe ser uno de: madera, tela, acero, etc
    estimated_price: float  # Debe ser > 100
    
    @validator('customer_email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email inválido')
        return v
    
    @validator('width', 'height', 'depth')
    def validate_dimensions(cls, v):
        if v <= 0:
            raise ValueError('Dimensiones deben ser positivas')
        if v > 500:
            raise ValueError('Dimensión muy grande (máx 500cm)')
        return v

@router.post("/orders")
async def create_order(order_data: OrderCreate, db: AsyncSession):
    """Pydantic valida automáticamente"""
    try:
        order = Order(**order_data.dict())
        db.add(order)
        await db.commit()
        return {"order_id": order.id, "status": "created"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
```

**Tiempo:** 1-2 horas

**Impacto:** MEDIO - Sin esto, datos corruptos pueden entrar

---

### 6. 🟠 INTEGRACIÓN CALCULATOR → BD (IMPORTANTE)

**Ubicación:** `frontend/` + `backend/app/api/`

**Actualmente:**
- ✅ Calculator HTML funciona
- ❌ Solo envía email manual
- ❌ No crea registro en BD

**Qué hacer:**

```
Cuando usuario calcula presupuesto:

ANTES:
├─ Calcula precio
├─ Usuario deja email
└─ ¿Envía email? (dudoso)

DEBE SER:
├─ Calcula precio
├─ Usuario deja email + nombre + teléfono
├─ Envía API POST /api/v1/orders con presupuesto
├─ Crea Lead en BD
├─ Envía email "Presupuesto listo" con:
│  ├─ Resumen del proyecto
│  ├─ Precio
│  ├─ "Confirmar" o "Modificar"
│  └─ Link a dashboard personal
└─ Admin recibe notificación
```

**Código necesario:**

```javascript
// Frontend (MentePausada + calculator)
async function submitPresupuesto() {
    const data = {
        customer_email: document.getElementById("email").value,
        customer_name: document.getElementById("name").value,
        customer_phone: document.getElementById("phone").value,
        width: sliders.width,
        height: sliders.height,
        depth: sliders.depth,
        material: dropdown.material,
        finish: dropdown.finish,
        estimated_price: totalPrice,
        source: "calculator"  // Tracking
    };
    
    const response = await fetch("/api/v1/orders", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });
    
    const result = await response.json();
    
    // Mostrar mensaje "Presupuesto enviado"
    showConfirmation(`Presupuesto $${totalPrice} enviado a ${data.customer_email}`);
}
```

**Tiempo:** 1-2 horas

**Impacto:** IMPORTANTE - Sin esto, leads no se guardan

---

## 📋 RESUMEN POLT MOBILIER

| Item | Status | Tiempo | Impacto |
|------|--------|--------|---------|
| Brand profile | ✅ 100% | 0h | - |
| Calculator | ✅ 80% | 0.5h | Conectar a BD |
| Database model | ✅ 100% | 0h | - |
| API routes | ✅ 80% | 0.5h | Agregar lógica |
| **Gestor-órdenes skill** | 🔴 0% | **2-3h** | **IMPORTANTE** |
| **Email automático** | 🔴 0% | **1-2h** | **IMPORTANTE** |
| **Dashboard BD** | 🔴 0% | **2-3h** | **IMPORTANTE** |
| **Contenido auto 9 AM** | 🔴 0% | **2-3h** | **IMPORTANTE** |
| **Validación input** | 🔴 0% | **1-2h** | MEDIO |
| **Calculator → BD** | 🔴 0% | **1-2h** | IMPORTANTE |

**TOTAL TRABAJO:** 10-18 horas = **2 sesiones (5-9h cada una)**

---

## 🎯 PLAN DE ACCIÓN POLT MOBILIER

### Sesión 1 (5 horas)

**Paso 1: Skill Gestor-Órdenes (2-3 horas)**
```
[ ] Crear archivo backend/app/agents/gestor_ordenes_polt.py
[ ] Implementar OrderManagerAgent con métodos:
    - create_order()
    - update_order_status()
    - upload_progress_photo()
[ ] Crear endpoints en api/orders.py:
    - POST /api/v1/orders/create
    - PUT /api/v1/orders/{id}/status
    - POST /api/v1/orders/{id}/photo
[ ] Test: Crear orden via API → Verificar en BD
```

**Paso 2: Email Automático (1-2 horas)**
```
[ ] Crear backend/app/email_polt_notifications.py
[ ] Implementar 5 templates (confirmación, producción, progreso, listo, entregado)
[ ] Crear función send_order_email_by_status()
[ ] Conectar con webhook: cuando status cambia → envía email
[ ] Test: Cambiar status → Email llega
```

**Paso 3: Validación (1 hora)**
```
[ ] Crear Pydantic models: OrderCreate, OrderUpdate
[ ] Agregar validación a endpoints
[ ] Test: Intentar crear orden con datos malos → error
```

### Sesión 2 (5 horas)

**Paso 1: Dashboard Conectado (2-3 horas)**
```
[ ] OPCIÓN A: Convertir HTML v5 a React
      [ ] Recrear como componente
      [ ] Conectar a /api/v1/orders
      [ ] Auto-refresh cada 1 minuto
   
   OPCIÓN B: Mejorar HTML + JavaScript
      [ ] Agregar fetch() para obtener órdenes
      [ ] Mostrar en tabla dinámica
      [ ] Botones para cambiar status
      
[ ] Test: Crear orden → Aparece en dashboard en tiempo real
```

**Paso 2: Contenido Automático 9 AM (2 horas)**
```
[ ] Crear backend/app/tasks/daily_content_polt.py
[ ] Implementar generador de carousel Instagram
[ ] Implementar newsletter email
[ ] Crear scheduled task que corre 9 AM cada día
[ ] Test: Ejecutar manualmente → Verificar que genera contenido
```

**Paso 3: Integración Calculator (1 hora)**
```
[ ] Modificar calculator HTML para hacer POST a /api/v1/orders
[ ] Agregar campos: nombre, teléfono
[ ] Test: Calcular presupuesto → Crear orden en BD
```

### Resultado: 🎉 **POLT COMPLETAMENTE AUTOMATIZADA**

---

## 💰 PROYECCIÓN POLT MOBILIER

Después de 2 sesiones:

```
Mes 1: 2-3 órdenes = $1k-3k
Mes 2: 4-6 órdenes = $2k-6k (contenido auto empieza tracción)
Mes 3: 8-12 órdenes = $4k-12k (marketing + boca a boca)
Mes 6: 15-20 órdenes/mes = $8k-15k/mes

Meta: 20 órdenes/mes @ $1000 promedio = $20k/mes
Timeline: 3-4 meses con inversión en ads
```

---

*Plan Polt Mobilier: 2 sesiones, 10-18 horas, FULL AUTOMATION 🚀*
