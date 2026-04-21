# Polt Mobilier - Flujo Detallado de Automatización

## 📋 Resumen Ejecutivo

Polt Mobilier es un **servicio de muebles personalizados**: diseño + fabricación bajo demanda.

- **Público:** Profesionales, diseñadores, personas con espacio limitado en LATAM
- **Modelo:** Consulta → Presupuesto → Orden → Producción → Entrega
- **Diferenciador:** Custom designs, acabados premium, producción local
- **Calculadora Web:** https://incredible-tapioca-c3c3f1.netlify.app/ (activa)
- **Objetivo:** 5-10 órdenes/mes a $500-2000 cada una

---

## 🔄 Flujo Completo del Cliente

### Fase 1: Generador de Leads (Content Marketing)

**Tarea Automatizada:** `daily-content-polt` (9 AM diariamente)

**Contenido Generado (4-5 piezas/día):**

#### Tipo 1: Before/After Showcases (2x/semana)
```
Instagram Carousel/Reel
├─ Slide 1: "Espacio problemático"
├─ Slide 2-3: Proceso de transformación
├─ Slide 4: "Resultado final"
└─ CTA: "¿Tu espacio necesita un cambio?"
```

#### Tipo 2: Tips & Educación (1x/semana)
```
Instagram Post
├─ Consejo de diseño: "Cómo elegir colores"
├─ o "Muebles para espacios pequeños"
├─ o "Tendencias 2026 en moblaje"
└─ CTA: "¿Preguntas? Usa nuestra calculadora"
```

#### Tipo 3: Success Stories (1x/semana)
```
Instagram Reel (30-60s video)
├─ Cliente describe problema
├─ Muestra mueble diseñado
├─ Cliente feliz con resultado
└─ CTA: "Manda tu proyecto"
```

#### Tipo 4: Email Newsletter (1x/semana)
```
Subject: "Proyecto de la semana: [nombre]"
├─ Historia del cliente
├─ Desafío + solución
├─ Fotos de antes/después
├─ Proceso de fabricación
└─ CTA: "¿Tienes un proyecto similar?"
```

#### Tipo 5: Behind-the-Scenes (1x/semana)
```
Instagram Stories/Reel
├─ Taller en acción
├─ Detalle de acabados
├─ Team working
└─ "Esto es lo que hace nuestro trabajo especial"
```

**Creador Humano Workflow:**
```
AI genera 5 piezas de contenido
  ↓
Creador revisa: ¿Menciona muebles correctos? ¿Historia convincente?
  ↓
Si OK: Aprueba
  ↓
Sistema auto-publica en Instagram + envía email newsletter
  ↓
Si requiere cambios: Devuelve a AI con feedback
```

---

### Fase 2: Lead Capture (Calculadora)

**Calculadora Web (Netlify)**
- URL: https://incredible-tapioca-c3c3f1.netlify.app/
- Propósito: Lead capture + presupuesto inicial

**Flow:**
```
Cliente ingresa:
├─ Tipo de mueble (silla, mesa, estantería, etc.)
├─ Dimensiones aproximadas
├─ Material preferido
├─ Estilo/color
└─ Presupuesto aproximado

Sistema calcula:
├─ Costo estimado (basado en fórmula)
├─ Timeline de producción
└─ "¿Te interesa? Ingresa tu email"

Lead capture:
├─ Email almacenado en BD
├─ Envía: "Gracias, aquí tu presupuesto estimado"
├─ Propone: "¿Quieres una consulta personalizada?"
└─ Incluye: Link a WhatsApp/email directo
```

---

### Fase 3: Consulta & Order Creation

**Skill:** `gestor-ordenes-polt`

**Flujo:**
```
Cliente solicita presupuesto personalizado
  (vía WhatsApp, email, o formulario web)

Skill: gestor-ordenes-polt analiza:
├─ Specs detalladas
├─ Foto del espacio (si disponible)
├─ Presupuesto máximo
└─ Timeline deseado

AI genera:
├─ Propuesta personalizada (precio final)
├─ Detalles técnicos
├─ Timeline estimado
├─ Opciones de personalización
└─ "¿Confirmas? Adelantamos la orden"

Si cliente confirma:
├─ Crea record Order en BD
├─ Asigna a productor disponible
├─ Envía: Email confirmación + orden number
└─ Status: "En espera de pago"
```

**Información de Orden**
```
Order Number: POL-20260417-001
Cliente: [nombre]
Producto: [tipo de mueble]
Dimensiones: [medidas exactas]
Material: [especificaciones]
Acabado: [color, stain, etc]
Costo estimado: $XXX
Costo final: [luego de producción]
Timeline: [semanas]
Productor asignado: [nombre]
```

---

### Fase 4: Producción & Comunicación

**Sistema de Notificaciones**

#### Email en Cada Hito:

**Email 1: Confirmación (Día 0)**
```
Subject: "Tu orden #POL-001 está confirmada ✓"

Hola {name},

Tu mueble está en la lista de producción.

Detalles:
- Mueble: {product}
- Dimensiones: {specs}
- Precio: ${cost}
- Productor: {producer_name}
- ETA: {estimated_date}

En 2 semanas te enviamos fotos del progreso.

¿Preguntas? Responde a este email.

Polt Mobilier
```

**Email 2: Progreso (Semana 2)**
```
Subject: "Tu {product} está tomando forma 🔨"

Hola {name},

¡Tenemos noticias! Tu mueble está en progreso.

[PHOTO_OF_WORK_IN_PROGRESS]

El taller estima completar en [X] días más.

¿Algún cambio? Responde rápido y lo ajustamos.

Polt Mobilier
```

**Email 3: Casi Listo (Semana 4)**
```
Subject: "Casi listo: Tu {product} en los últimos detalles ✨"

Hola {name},

Tu mueble está en los últimos detalles. Acabados finales en progreso.

[PHOTO_OF_NEARLY_COMPLETE]

Entrega estimada: {delivery_date}

¿Horario de entrega? Responde para coordinar.

Polt Mobilier
```

**Email 4: Listo para Entrega (Día anterior)**
```
Subject: "¡Tu {product} está listo! 🎉 Entrega mañana"

Hola {name},

¡Llegó el momento! Tu mueble está listo.

Entrega: {delivery_date} entre {time_window}
Dirección: {delivery_address}
Contacto: {phone_for_delivery}

¿Horario confirma?

Polt Mobilier
```

**Email 5: Post-Entrega Satisfacción**
```
Subject: "¿Cómo está tu {product}? Nos importa tu opinión 💭"

Hola {name},

Tu mueble fue entregado hace 3 días. ¿Qué tal?

Nos encantaría saber:
- ¿Se ajusta perfecto a tu espacio?
- ¿Calidad de acabado?
- ¿Algún ajuste necesario?

Responde y, si necesitas algo, lo solucionamos.

Upsell (opcional):
¿Necesitas más muebles? Tenemos referencias para restauración.

Polt Mobilier
```

---

### Fase 5: Dashboard de Producción

**Skill:** `polt-production-dashboard`

**Visible para:**
- Productor (asignado a orden)
- Manager (supervisión general)
- Cliente (tracking simplificado)

**Estados de Orden:**
```
1. En espera    → Esperando confirmación pago
2. En progreso  → En el taller
3. Casi listo   → Últimos detalles
4. Listo        → Listo para entrega
5. Entregado    → Completado
6. Retrasado    → Delayed (auto-alert si > ETA)
```

**Información Visible por Status:**
```
En progreso:
├─ Fotos de avance
├─ % de completitud
├─ Días restantes
├─ Detalles técnicos en proceso
└─ Cualquier cambio o ajuste

Casi listo:
├─ Foto final (antes de entrega)
├─ Última fecha ETA
├─ Detalles de entrega
└─ Confirmación cliente de horario

Retrasado:
├─ Razón del retraso
├─ Nuevo ETA
├─ Comunicación enviada a cliente
└─ Acción correctiva
```

---

## 🛠️ Integración Técnica

### Base de Datos (Schema)

```sql
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_number VARCHAR(20) UNIQUE NOT NULL,
  
  -- Cliente
  customer_email VARCHAR(255) NOT NULL,
  customer_name VARCHAR(255) NOT NULL,
  customer_phone VARCHAR(20),
  
  -- Producto
  product_type VARCHAR(100) NOT NULL,
  custom_specs TEXT NOT NULL,
  material VARCHAR(100),
  color_finish VARCHAR(100),
  
  -- Presupuesto
  estimated_cost DECIMAL(10,2),
  final_cost DECIMAL(10,2),
  payment_status VARCHAR(20) DEFAULT 'pending',  -- paid/pending
  
  -- Producción
  status VARCHAR(20) DEFAULT 'en_espera',
  assigned_producer VARCHAR(255),
  start_date DATETIME,
  estimated_delivery DATETIME,
  actual_delivery DATETIME,
  
  -- Comunicación
  email_sent_count INTEGER DEFAULT 0,
  last_notification_at DATETIME,
  whatsapp_sent BOOLEAN DEFAULT false,
  
  -- Fotos/documentación
  work_photos TEXT,  -- JSON array of URLs
  final_photo_url VARCHAR(500),
  
  -- Seguimiento
  is_delayed BOOLEAN DEFAULT false,
  delay_reason VARCHAR(255),
  
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_order_number ON orders(order_number);
CREATE INDEX idx_customer_email ON orders(customer_email);
CREATE INDEX idx_status ON orders(status);
```

### API Endpoints

**Create Order**
```
POST /api/orders/create
Input: {
  customer_email: "email@example.com",
  customer_name: "Juan",
  product_type: "silla personalizada",
  custom_specs: "Dimensiones 80x60x90cm, madera roble...",
  estimated_cost: 1200.00
}
Output: {
  order_number: "POL-20260417-001",
  created_at: "2026-04-17T09:00:00Z"
}
```

**Update Order Status**
```
PUT /api/orders/{order_number}/status
Input: {
  status: "en_progreso|casi_listo|listo|entregado",
  work_photo_url: "https://...",
  notes: "Detalles del estado"
}
Action:
  1. Actualiza status en BD
  2. Si status cambió: envía email a cliente
  3. Si is_delayed && status != listo: alerta al manager
```

**Analytics**
```
GET /api/orders/analytics
Output: {
  active_orders: X,
  completed_this_month: X,
  revenue_this_month: $XXX,
  avg_production_time: X days,
  delayed_orders: X,
  customer_satisfaction: X%
}
```

---

## 📅 Tareas Automatizadas

| Tarea | Hora | Qué hace |
|-------|------|----------|
| `daily-content-polt` | 9 AM | Genera + publica 5 piezas content |
| `daily-polt-analytics` | 5 PM | Reporte: órdenes, retrasos, revenue |
| `email-sequence-orders` | 2 AM, 8 AM, 2 PM, 8 PM | Envía emails por hito de orden |

---

## 🎯 Key Metrics

1. **Active Orders:** Target 5-10 en paralelo
2. **On-Time Delivery:** Target >90%
3. **Production Time:** Avg 3-4 semanas (personalizado)
4. **Customer Satisfaction:** Target >4.5/5 (encuesta post-entrega)
5. **AOV (Average Order Value):** Target $800-1500
6. **Revenue:** Target $4,000-15,000/mes

---

## ⚠️ Problemas Comunes

| Problema | Solución |
|----------|----------|
| Órdenes retrasadas | Revisar capacidad taller, asignar mejor, comunicar rápido |
| Bajo lead volume | Fortalecer content en Instagram, ads opcional |
| AOV bajo | Promover upgrades (material premium, customizaciones) |
| Cliente insatisfecho | Seguimiento personal post-entrega, opciones de ajuste |

---

## 📈 Roadmap (Próximas 4 semanas)

- **Semana 1:** Content automation activo (9 AM diario)
- **Semana 2:** Sistema de notificaciones activo (emails por hito)
- **Semana 3:** Dashboard de producción en uso
- **Semana 4:** Analytics + optimizaciones

---

*Actualizado: 2026-04-17*
