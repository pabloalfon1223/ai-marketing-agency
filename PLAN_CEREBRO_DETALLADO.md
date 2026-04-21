# 🧬 PLAN CEREBRO - ANÁLISIS DETALLADO

**Objetivo:** Sistema continuo de ideación para identificar/validar proyectos alcanzables $20-50k/mes  
**Modelo:** Ideas → Validación → MVP tracking → $20k escalable  
**Timeline:** 2-3 sesiones (6-8 horas) = SISTEMA COMPLETO  
**Estado actual:** 0% implementación (arquitectura lista, código pendiente)

---

## ✅ QUÉ TIENE (Arquitectura y Diseño)

### 1. ARQUITECTURA DEFINIDA ✅

**Ubicación:** Documentación en planes anteriores

```
Fase 1: GENERACIÓN de ideas
  → Input: (tiempo disponible, capital, skills propios)
  → Output: 20-50 ideas multi-tipo
  → Ranking: por potencial $20k+/mes

Fase 2: VALIDACIÓN de mercado
  → Busca: Google Trends, Reddit, Quora, ProductHunt
  → Analiza: competencia, TAM, pricing
  → Score: 0-100 viabilidad
  → Output: MVP mínimo + 3 formas de lanzar

Fase 3: TRACKING y decisiones
  → Dashboard: ideas | score | tipo | tiempo a $20k | status
  → Histórico: qué funcionó, qué falló, learnings
  → Tareas semanales: trending ideas
  → Tareas mensuales: retrospective + decisiones
```

**Status:** ✅ Arquitectura clara y documentada

---

### 2. MODELOS DE DATOS CLAROS ✅

**Concepto de tabla Idea (no implementado aún):**

```python
class Idea:
    id: int
    title: str
    description: str
    type: enum  # "SaaS", "servicio", "e-commerce", "creator", "híbrido"
    potential_revenue: int  # Estimado $20k+/mes
    capital_required: int  # Inversión inicial
    timeline_to_20k: str  # "1 mes", "3 meses", "6 meses"
    viability_score: int  # 0-100
    market_demand: str  # Alto, Medio, Bajo
    competition: str  # Análisis competitivo
    created_at: datetime
    validated_at: datetime | null
    status: enum  # "cruda", "validación", "MVP", "$20k track", "descartada", "pivotada"
    mvp_hypothesis: str  # Qué asumir para validar
    validated_by: str  # User que validó
    learnings: str  # Qué aprendimos
```

**Status:** ✅ Schema claro

---

### 3. TIPOS DE IDEAS DEFINIDOS ✅

**Categorías a generar:**

```
1. SaaS ($20-100k/mes)
   - Herramientas B2B/B2C
   - Subscripción mensual
   - Ejemplo: Herramienta de analytics para creadores
   
2. Servicios ($20-50k/mes)
   - Consultoría, agencia, coaching
   - Modelo: Proyecto + retainer
   - Ejemplo: Consultoría IA para empresas
   
3. E-commerce ($20-50k/mes)
   - Productos físicos/digitales
   - Dropshipping, POD, físico
   - Ejemplo: Curso especializado + comunidad
   
4. Creator ($20-30k/mes)
   - YouTube, TikTok, Instagram, newsletter
   - Modelo: Ads + sponsors + productos propios
   - Ejemplo: Newsletter de ideas de negocio
   
5. Híbridos ($50k+/mes)
   - Combinación de los anteriores
   - Ejemplo: SaaS + Consulting + Community
```

**Status:** ✅ Tipos documentados

---

## ❌ QUÉ FALTA (3 Bloqueadores Críticos)

### BLOQUEADOR #1: SKILLS NO IMPLEMENTADOS
**Severidad:** 🔴 CRÍTICO  
**Tiempo:** 2-3 horas

#### Skill #1: "generador-ideas-cerebro"

**Qué necesita:**

```python
# backend/app/agents/ideas_generator.py (NUEVO)

class IdeasGeneratorAgent:
    """
    Genera 20-50 ideas alcanzables en $20-50k/mes basado en inputs del usuario
    """
    
    def generate_ideas(
        self, 
        available_time: str,  # "10 horas/semana", "full-time"
        available_capital: int,  # $5000, $50000, ilimitado
        my_skills: List[str],  # ["programación", "marketing", "diseño"]
        interests: List[str] = None  # ["IA", "bienestar", "educación"]
    ) -> List[dict]:
        """
        Output format:
        [
            {
                "title": "AI Writing Coach for Creators",
                "description": "SaaS que ayuda a creators a escribir mejor",
                "type": "SaaS",
                "potential_revenue": 25000,  # $/mes a escala
                "capital_required": 2000,
                "timeline_to_20k": "2 meses",
                "reasoning": "Alta demanda en creadores, bajo CAC con TikTok",
                "target_market": "Creadores de contenido 50k+ followers",
                "mvp": "ChatGPT + Telegram bot + 10 beta users"
            },
            ...
        ]
        """
```

**Implementación:**

- [ ] Crear archivo: `backend/app/agents/ideas_generator.py`
- [ ] Implementar método `generate_ideas()`
  - Usar template de 50+ ideas (almacenadas en template)
  - Filtrar por skills del usuario
  - Filtrar por capital disponible
  - Rankear por "tiempo a $20k"
- [ ] Crear endpoint: `POST /api/v1/ideas/generate`
  - Input: available_time, capital, skills, interests
  - Output: Lista de ideas ordenada por viabilidad
- [ ] Test: 
  - Input: "20h/week, $10k, programación+marketing"
  - Output: 20-50 ideas relevantes ordenadas

**Status:** 0% implementado

---

#### Skill #2: "validador-mercado-cerebro"

**Qué necesita:**

```python
# backend/app/agents/market_validator.py (NUEVO)

class MarketValidatorAgent:
    """
    Valida idea de negocio buscando demanda real de mercado
    Retorna score 0-100 de viabilidad
    """
    
    def validate_idea(self, idea: dict) -> dict:
        """
        Busca:
        1. Google Trends: búsquedas relacionadas últimos 3 meses
        2. Reddit: posts en r/[topic] (actividad, sentimiento)
        3. ProductHunt: productos similares, scores
        4. Quora: preguntas no respondidas (pain point)
        5. TikTok/YouTube: búsquedas, visualizaciones
        
        Output:
        {
            "idea_title": "AI Writing Coach",
            "market_demand": "Alto",  # Alto, Medio, Bajo
            "google_trends_interest": 78,  # 0-100
            "reddit_activity": 45,  # posts/mes
            "competition_level": "Media",  # Baja, Media, Alta
            "similar_products": [
                {"name": "Copy.ai", "pricing": "$49/mes", "reviews": 4.2}
            ],
            "gaps_identified": [
                "No hay product para creators específicamente",
                "Herramientas genéricas, no especializadas"
            ],
            "mvp_hypothesis": [
                "ChatGPT API + Telegram bot = $0 MVP",
                "Validar con 10 beta testers creadores",
                "Si 7/10 pagan, escalar a SaaS"
            ],
            "viability_score": 78,  # Escala 0-100
            "recommendation": "Validar en 2 semanas antes de MVP"
        }
        """
```

**Implementación:**

- [ ] Crear archivo: `backend/app/agents/market_validator.py`
- [ ] Implementar integraciones:
  - Google Trends API: Buscar tendencias
  - Reddit API: Buscar actividad en comunidades
  - ProductHunt API: Productos competencia
  - Web scraping (Quora, YouTube): Búsquedas sin responder
- [ ] Crear endpoint: `POST /api/v1/ideas/{idea_id}/validate`
  - Input: Idea ID
  - Output: Reporte completo de validación + score
- [ ] Test:
  - Input: Idea "AI Writing Coach"
  - Output: Score 70-90, reporte detallado

**Status:** 0% implementado

---

### BLOQUEADOR #2: DASHBOARD NO EXISTE
**Severidad:** 🔴 CRÍTICO  
**Tiempo:** 2 horas

**Ubicación:** `frontend/src/pages/CerebroDashboard.tsx` (NUEVO)

**Qué necesita:**

```tsx
// Layout con 3 secciones:

// 1. GENERADOR (lado izquierdo, form)
<IdeasGeneratorForm />
  ├── Input: Horas disponibles (dropdown)
  ├── Input: Capital ($)
  ├── Input: Skills (multi-select)
  ├── Input: Intereses (multi-select)
  ├── Botón: "Generar ideas"
  └── Loading state mientras genera

// 2. LISTADO DE IDEAS (centro, tabla)
<IdeasTable />
  ├── Columnas: Título | Score | Tipo | $20k Timeline | Status
  ├── Filtros: Por tipo, por score (>70), por status
  ├── Click fila: Abre detalle en panel
  ├── Acción: "Validar" → Corre skill validador
  ├── Acción: "Descartar" → Marca como descartada
  └── Acción: "MVP" → Abre diálogo para crear seguimiento

// 3. DETALLE DE IDEA (lado derecho, panel)
<IdeaDetail />
  ├── Descripción completa
  ├── Target market
  ├── MVP hypothesis
  ├── Learnings (si existe validación)
  ├── Timeline a $20k
  ├── Capital requerido
  ├── Validación: 
  │   ├── Score actual
  │   ├── Demanda de mercado
  │   ├── Competencia
  │   └── Gaps identificados
  └── Historial: Cuándo se creó, cuándo se validó
```

**Estructura de datos para dashboard:**

```javascript
{
  ideas: [
    {
      id: 1,
      title: "AI Writing Coach",
      description: "...",
      type: "SaaS",
      score: 78,
      status: "validated",  // cruda, validación, MVP, $20k, descartada
      created_at: "2026-04-18",
      validated_at: "2026-04-20",
      validation_data: { ... },
      learnings: "..."
    }
  ],
  stats: {
    total_ideas: 45,
    validated_count: 12,
    high_score_count: 8,
    in_mvp: 2,
    in_20k_track: 1
  }
}
```

**Implementación:**

- [ ] Crear componente React: `IdeaGeneratorForm`
- [ ] Crear componente React: `IdeasTable` con filtros
- [ ] Crear componente React: `IdeaDetail` con validación
- [ ] Conectar a APIs:
  - GET `/api/v1/ideas` - Lista todas
  - POST `/api/v1/ideas/generate` - Genera nuevas
  - POST `/api/v1/ideas/{id}/validate` - Valida
  - PUT `/api/v1/ideas/{id}` - Actualiza status
- [ ] Styling: Tabla limpia, colores por status, responsive

**Status:** 0% implementado

---

### BLOQUEADOR #3: TAREAS PROGRAMADAS NO EXISTEN
**Severidad:** 🔴 CRÍTICO  
**Tiempo:** 1-2 horas

#### Tarea #1: "weekly-trending-ideas"

**Qué necesita:**

```python
# backend/app/tasks/weekly_trending_ideas.py (NUEVO)

async def weekly_trending_ideas_task():
    """
    Corre automáticamente: Lunes 8 AM
    
    1. Busca trending en:
       - Google Trends (últimos 7 días)
       - ProductHunt (nuevos launches)
       - Twitter/X trending
       - Reddit rising posts
       - LinkedIn trending
       - TikTok trending
    
    2. Para cada trending:
       - Identifica oportunidad de negocio
       - Genera 10 ideas que capitalicen trend
       - Score estimado de viabilidad
    
    3. Output: Reporte markdown
       - Título: "Trending Ideas - Semana del 2026-04-21"
       - 10+ ideas nuevas con score
       - Descarta ideas que bajaron en demanda
       - Propone 3 ideas para focus esta semana
    
    4. Guarda en:
       - DB: Inserta ideas como "status: cruda"
       - File: reports/weekly_trending_2026-04-21.md
       - Notificación: Email al usuario
    """
```

**Implementación:**

- [ ] Crear archivo: `backend/app/tasks/weekly_trending_ideas.py`
- [ ] Implementar búsquedas:
  - Google Trends API
  - Reddit API: r/[trending_topics]
  - ProductHunt API: Nuevos productos
  - Web scraping: LinkedIn, Twitter
- [ ] Crear scheduled task:
  - Trigger: Lunes 8 AM
  - Comando: Ejecutar función async
- [ ] Output:
  - Guarda ideas en BD
  - Genera reporte markdown
  - Envía email al usuario
- [ ] Test:
  - Ejecutar manualmente
  - Verificar que genera 10+ ideas
  - Verificar que score es razonable

**Status:** 0% implementado

---

#### Tarea #2: "cerebro-retrospective-monthly"

**Qué necesita:**

```python
# backend/app/tasks/monthly_cerebro_retrospective.py (NUEVO)

async def monthly_retrospective_task():
    """
    Corre automáticamente: 1° del mes, 9 AM
    
    Análisis de todo el mes anterior:
    
    1. Ideas que fallaron:
       - Cuál era el score?
       - Qué se asumió que fue incorrecto?
       - Cuál fue el gap?
       → Learnings para mejorar validación
    
    2. Ideas que funcionaron:
       - Cuáles pasaron $20k/mes?
       - Cuál fue el patrón de éxito?
       - Qué hicimos bien?
       → Patterns a repetir
    
    3. Ideas en validación:
       - Cuántas siguen en track?
       - Cuáles pivotar vs descartar?
       → Decisiones para mes siguiente
    
    4. Métricas:
       - Ideas generadas este mes: N
       - Ideas validadas: N
       - Tasa pivot vs muerte: X%
       - Ideas escaladas a $1k+: N
    
    5. Decisiones para próximo mes:
       - 3 ideas a enfoque especial
       - Capital a invertir en ads
       - Cuál skill mejorar?
    
    Output: Reporte markdown detallado
    """
```

**Implementación:**

- [ ] Crear archivo: `backend/app/tasks/monthly_cerebro_retrospective.py`
- [ ] Queries a BD:
  - Ideas descartadas (motivo, score, learnings)
  - Ideas en $20k track (ingresos actuales)
  - Ideas nuevas (cuántas generadas)
- [ ] Análisis:
  - Calcular tasa de éxito
  - Identificar patterns de éxito
  - Identificar motivos de fallo
- [ ] Generar reporte:
  - Métricas cuantitativas
  - Análisis cualitativo
  - Recomendaciones para próximo mes
- [ ] Scheduled task:
  - Trigger: 1° de mes, 9 AM
  - Output: Reporte + notificación

**Status:** 0% implementado

---

## 🎯 ACTION PLAN (Paso a Paso)

### Sesión 1: GENERACIÓN + VALIDACIÓN (2-3 horas)

**Paso 1: Crear modelos en BD (30 min)**

```
[ ] Archivo: backend/app/models/idea.py
    [ ] Clase Idea con todos los campos
    [ ] Campos computed: days_since_created, status_color
    [ ] Validaciones: score 0-100, timeline válido
    
[ ] Ejecutar migraciones:
    [ ] SQLAlchemy: Base.metadata.create_all (auto)
    [ ] Verificar en sqlite3 que existe tabla "ideas"
```

**Paso 2: Crear skill generador-ideas (1 hora)**

```
[ ] Archivo: backend/app/agents/ideas_generator.py
    [ ] Clase IdeasGeneratorAgent
    [ ] Template de 50+ ideas predefinidas
    [ ] Método generate_ideas() que filtra por skills/capital
    [ ] Ranking por "tiempo a $20k"

[ ] Crear endpoint: POST /api/v1/ideas/generate
    [ ] Recibe: available_time, capital, skills
    [ ] Retorna: Lista ideas + scores
    [ ] Test: curl + JSON

[ ] Test manual:
    [ ] Input: "20h/semana, $10k, python+marketing"
    [ ] Verificar: 20+ ideas, highest score primero
```

**Paso 3: Crear skill validador-mercado (1-1.5 horas)**

```
[ ] Archivo: backend/app/agents/market_validator.py
    [ ] Clase MarketValidatorAgent
    [ ] Métodos: 
        [ ] search_google_trends()
        [ ] search_reddit()
        [ ] search_product_hunt()
        [ ] calculate_score()

[ ] Crear endpoint: POST /api/v1/ideas/{id}/validate
    [ ] Recibe: Idea ID
    [ ] Ejecuta validación
    [ ] Retorna: Score + reporte
    [ ] Actualiza BD con validation_data

[ ] Test manual:
    [ ] Seleccionar una idea
    [ ] Validar
    [ ] Verificar score 0-100 + reporte
```

**Resultado:** 20+ ideas generadas, 5-10 validadas, scores calculados ✅

---

### Sesión 2: DASHBOARD + TAREAS AUTOMÁTICAS (2-3 horas)

**Paso 1: Crear dashboard React (1.5 horas)**

```
[ ] Archivo: frontend/src/pages/CerebroDashboard.tsx
    [ ] Componente IdeaGeneratorForm
    [ ] Componente IdeasTable con filtros
    [ ] Componente IdeaDetail
    
[ ] Conectar a APIs:
    [ ] GET /api/v1/ideas
    [ ] POST /api/v1/ideas/generate
    [ ] POST /api/v1/ideas/{id}/validate
    [ ] PUT /api/v1/ideas/{id}

[ ] Styling:
    [ ] Colores por tipo (SaaS: azul, Servicio: verde, etc)
    [ ] Colores por status (cruda: gris, validada: verde)
    [ ] Tabla responsive
    [ ] Modals para detalles

[ ] Test:
    [ ] Abrir en navegador
    [ ] Generar ideas
    [ ] Validar una
    [ ] Cambiar status
    [ ] Filtrar por score
```

**Paso 2: Crear tareas programadas (1 hora)**

```
[ ] Archivo: backend/app/tasks/weekly_trending_ideas.py
    [ ] Función async que busca trends
    [ ] Genera 10+ ideas nuevas
    [ ] Inserta en BD
    [ ] Trigger: Lunes 8 AM

[ ] Archivo: backend/app/tasks/monthly_cerebro_retrospective.py
    [ ] Análisis de mes anterior
    [ ] Calcul de métricas
    [ ] Recomendaciones
    [ ] Trigger: 1° mes 9 AM

[ ] Registrar tareas en scheduler:
    [ ] En main.py o tasks/scheduler.py
    [ ] Test manual: Ejecutar función
```

**Paso 3: Integration test (30 min)**

```
[ ] Test flujo completo:
    1. Abrir dashboard
    2. Generar ideas
    3. Validar 3 ideas
    4. Ver scores actualizados
    5. Filtrar por tipo
    6. Cambiar status a "MVP"
    7. Verificar en tabla

[ ] Test tareas:
    1. Ejecutar manualmente weekly_trending
    2. Verificar ideas insertadas
    3. Ejecutar manualmente monthly_retrospective
    4. Verificar reporte generado
```

**Resultado:** Dashboard funcional, tareas automáticas corriendo ✅

---

### Sesión 3 (OPCIONAL): REFINAMIENTO (1-2 horas)

```
[ ] Mejorar validador:
    [ ] Agregar más fuentes (Quora, YouTube)
    [ ] Mejorar scoring algorithm
    [ ] Agregar confidence intervals
    
[ ] Mejorar generador:
    [ ] Template de ideas mejoradas
    [ ] Agregar más tipos (SaaS B2B, B2C, etc)
    [ ] Filtros más inteligentes
    
[ ] Dashboard: 
    [ ] Gráficos de trends
    [ ] Exportar ideas a PDF
    [ ] Compartir con colegas
    
[ ] Optimización:
    [ ] Cache de resultados
    [ ] Logging y debugging
```

---

## 📊 MATRIZ DE IMPLEMENTACIÓN

| Componente | Archivo | Tiempo | Prioridad | Status |
|-----------|---------|--------|-----------|--------|
| Modelo Idea | `models/idea.py` | 30 min | 🔴 | ❌ |
| Skills Generador | `agents/ideas_generator.py` | 1h | 🔴 | ❌ |
| Skills Validador | `agents/market_validator.py` | 1.5h | 🔴 | ❌ |
| Dashboard React | `pages/CerebroDashboard.tsx` | 1.5h | 🔴 | ❌ |
| Tarea Weekly | `tasks/weekly_trending_ideas.py` | 1h | 🟠 | ❌ |
| Tarea Monthly | `tasks/monthly_retrospective.py` | 30m | 🟠 | ❌ |
| **TOTAL** | **6 archivos nuevos** | **6-7h** | | |

---

## 💰 PROYECCIÓN CEREBRO (Escalable a $20-50k/mes)

### MES 1: GENERACIÓN + VALIDACIÓN
```
Semana 1: Implementar sistema (sesión 1-2)
  → 50 ideas generadas
  → 10 ideas validadas (score >70)
  
Semana 2-4: Refinamiento + tareas automáticas
  → Weekly task: 10+ ideas trending por semana
  → Manual validation: 5-10 ideas/semana
  → Total ideas: 100+
  → Top 10 ideas con score >75
  
Resultado: Dashboard operativo, pipeline de ideas lista
```

### MES 2-3: MVP VALIDATION
```
Tomar top 3 ideas y validar con usuarios reales
Cada idea:
  → MVP hipótesis probada
  → 10-20 beta users
  → Si 50%+ interés → Pasar a chat separado de implementación
  
Proyección: 1-2 ideas con potencial $20k+/mes
```

### MES 4-6: ESCALAMIENTO
```
Las ideas validadas se escalan en chats separados
Cerebro continúa:
  → Generando nuevas ideas semanalmente
  → Validando oportunidades mensuales
  → Identificando trends antes que competencia

Proyección: 
  → Pipeline de 200+ ideas documentadas
  → 20+ ideas validadas
  → 3-5 ideas en MVP/test
  → 1-2 ideas escaladas a $10k+/mes (camino a $20k+)
```

### AÑO 1 COMPLETO
```
Si ejecutamos bien:
  → Idea #1: $20k+/mes (SaaS o servicio)
  → Idea #2: $10k+/mes (E-commerce o creator)
  → Idea #3: $5k+/mes (Híbrido)
  
TOTAL: $35k+/mes base
+ Mente Pausada ($10-20k/mes)
+ Polt Mobilier ($10-20k/mes)

TOTAL SISTEMA: $55k-75k/mes
```

---

## 🔄 RELACIÓN CON OTROS PROYECTOS

**Mente Pausada** genera:
- Learnings sobre email + ads que aplican a ideas
- Revenue que financia validación de ideas
- Audience que puede ser beta tester de ideas

**Polt Mobilier** genera:
- Casos de éxito de servicios personalizados
- Modelo de producción que aplica a ideas
- Ejemplos de MVP rápido

**Cerebro** alimenta:
- Identificar nuevos mercados para ambos proyectos
- Detectar cuando Mente Pausada/Polt saturan
- Proponer pivots si algo no funciona

---

## 📋 CHECKLIST PRE-IMPLEMENTACIÓN

Antes de empezar sesión 1:

- [ ] Backend repo actualizado
- [ ] Database conectada y funcionando
- [ ] Stripe keys configuradas (aunque no se usen en Cerebro)
- [ ] FastAPI servidor corriendo sin errores
- [ ] React build en verde
- [ ] Verificar que API v1 routes están todas registradas

---

## 🚀 SIGUIENTES PASOS

**Decisión:** ¿Cuál chat empezar primero?

### RECOMENDACIÓN PRIORIDAD:

1. **Chat 1: MENTE PAUSADA** ← PRIMERO
   - Objetivo: VENDER PRIMER PRODUCTO
   - Tiempo: 1 sesión (3-4h)
   - ROI: $99-199 por compra
   - Financia los otros chats

2. **Chat 2: POLT MOBILIER** ← SEGUNDO
   - Objetivo: AUTOMATIZAR ÓRDENES
   - Tiempo: 2 sesiones (4-6h)
   - ROI: $500-2k por orden
   - Usa dinero de Mente Pausada

3. **Chat 3: CEREBRO** ← TERCERO
   - Objetivo: VALIDAR IDEAS ESCALABLES
   - Tiempo: 2-3 sesiones (6-8h)
   - ROI: $20-50k/mes potencial
   - Financia con dinero de #1 y #2

**Por qué este orden:**
- Mente Pausada genera dinero RÁPIDO (semana 1)
- Polt escala con dinero de Mente Pausada (semana 2-3)
- Cerebro explora opciones sin presión (semana 4+)

---

*Plan Cerebro: 2-3 sesiones, 6-8 horas, SISTEMA CONTINUO DE IDEACIÓN 🚀*

*Actualizado: 2026-04-18*
*Estado: Listo para implementación*
*Bloqueadores: Todos manejables en 1-2 chats dedicados*
