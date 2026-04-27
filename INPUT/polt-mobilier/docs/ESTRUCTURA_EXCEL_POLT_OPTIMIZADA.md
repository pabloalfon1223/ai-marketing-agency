# ESTRUCTURA OPTIMIZADA DE EXCEL PARA POLT MOBILIER

*Basada en tu flujo comprobado de Mente Pausada, adaptado a Polt*

---

## 🔄 TU FLUJO ACTUAL (Mente Pausada) → ADAPTADO A POLT

### Hoja 1: **IDEAS CRUDAS** (Brainstorm inicial)
Donde Lucas captura ideas sin filtro, después las completa:

| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| # | Auto | 1, 2, 3... | ID del item |
| Formato | Dropdown | Post / Carrusel / Reel | Tipo de contenido |
| Gancho (texto exacto) | Texto | "Tu ropa merece un lugar..." | Hook/título que detiene scroll |
| PILAR | Dropdown | Producto / Proceso / Soluciones | De qué pilar es (6 pilares) |
| ETAPA BUYER | Dropdown | TOFU / MOFU / BOFU | Dónde está el cliente (awareness/consideration/decision) |
| Idea breve | Texto largo | "Mostrar antes/después de placar" | Idea sin desarrollar |
| Estado | Dropdown | Crudo / En desarrollo / Listo | ¿Avanzó a la hoja Claude? |
| PRODUCTO/CATEGORÍA | Dropdown | Placar / Biblioteca / Escritorio / Restauración | Qué producto destacar |
| NOTAS RÁPIDAS | Texto | "Usar cliente Sara, cambio total" | Notas propias |

**Uso:** Ideas sin pulir. Cuando la idea está completa → se copia a la hoja **CLAUDE**.

---

### Hoja 2: **CLAUDE** (Contenido base para agentes + publicación)
Acá goes TODO armado, listo para publicar o pasar a generadores IA:

| Columna | Tipo | Ejemplo | Descripción |
|---------|------|---------|-------------|
| # | Auto | 1, 2, 3... | ID único |
| FALTA | Dropdown | ✅ Completo / ⚠️ Falta video / ⚠️ Falta copy | Qué falta para publicar |
| Formato | Dropdown | Post / Carrusel / Reel | Tipo de contenido |
| Gancho (texto exacto) | Texto | "Tu ropa merece un lugar..." | Texto EXACTO que va en post |
| PILAR | Dropdown | Producto / Proceso / Inspiración / Soluciones / Social proof / Promo | De los 6 pilares |
| ETAPA BUYER | Dropdown | TOFU / MOFU / BOFU | Fase del customer journey |
| Estado | Dropdown | Borrador / Listo para publicar / Publicado / En edición video | Estado actual |
| Guion/Copy (cuerpo + CTA) | Texto largo | Full copy del post | Texto COMPLETO que se publica |
| **PROMPT IMAGEN IA** | Texto largo | "Habitación minimalista, placar piso a techo..." | Para Nano Banana / Freepik |
| Escenas detalladas | Texto largo | JSON o descripción | Si es Reel: escenas, transiciones, duración |
| Audio / Sonido | Texto | "Musica: [nombre]" o "Voz en off: texto" | Qué audio usa |
| Caption con hashtags | Texto | Full caption con 10-15 hashtags | Caption IG + hashtags |
| KEYWORD | Texto | "muebles a medida, placar, diseño" | Para SEO |
| **PROMPT JSON (para Kling 2.5/CapCut)** | JSON | Ver abajo | Estructura para edición de video |
| FECHA PUBLICACIÓN | Fecha | 2026-04-15 | Cuándo publicar |
| ESTADO MEDIOS | Dropdown | Imagen lista / Video en edición / Listo / Publicado | Progreso multimedia |

---

### Hoja 3: **CALENDARIO CONTENIDO** (Vista macro)
Overview semanal/mensual:

| Columna | Tipo | Ejemplo |
|---------|------|---------|
| Día y Fecha | Fecha | Lunes 14/04 |
| Formato | Dropdown | Reel / Post / Carrusel |
| PILAR | Dropdown | Producto |
| Gancho (mini) | Texto | "Tu ropa merece..." |
| Estado | Dropdown | Publicado / Listo / En edición |

**Uso:** Lucas ve de un vistazo qué está programado.

---

### Hoja 4: **ANALYTICS** (Métricas + Decisiones)
Después de publicar, trackea resultados:

| Columna | Tipo | Ejemplo | Fórmula |
|---------|------|---------|---------|
| ID Post | Número | 1 | Link a CLAUDE |
| Fecha Publicación | Fecha | 2026-04-14 | |
| Formato | Dropdown | Reel | |
| Pilar | Dropdown | Producto | |
| Reach | Número | 2500 | Manual desde IG Insights |
| Impressions | Número | 3200 | Manual |
| Engagement (Likes + Comments + Saves) | Número | 120 | Manual |
| Engagement Rate % | % | 3.75% | =Engagement/Impressions |
| Clicks a WhatsApp | Número | 15 | Manual o pixel |
| Conversión (Consultas) | Número | 3 | Manual |
| CTR % | % | 0.47% | =Clicks/Impressions |
| MEJOR MOMENTO PUBLICACIÓN | Hora | 9am | Decisión basada en datos |
| OBSERVACIONES | Texto | "Reel corto funcionó mejor" | Lucas anota |

---

## 📋 ESTRUCTURA DETALLADA: PROMPT JSON (Para Kling 2.5 / CapCut / Remotion)

Cuando es un **REEL**, la columna "PROMPT JSON" contiene esto:

```json
{
  "formato": "reel",
  "duracion_segundos": 25,
  "orientacion": "vertical",
  "fps": 30,
  "resolucion": "1080x1920",
  "escenas": [
    {
      "numero": 1,
      "duracion": 5,
      "tipo": "visual_fija",
      "prompt_imagen": "Habitación vacía, pared blanca, piso de madera",
      "texto_overlay": "Tu espacio merece funcionar",
      "texto_posicion": "center_top",
      "fuente": "Sans-serif, bold, 48px",
      "color_texto": "#ffffff",
      "transicion_salida": "fade",
      "duracion_transicion": 0.5
    },
    {
      "numero": 2,
      "duracion": 8,
      "tipo": "visual_movimiento",
      "prompt_imagen": "Placar piso a techo, madera clara, abierto mostrando interior organizado",
      "movimiento": "pan_derecha",
      "velocidad_movimiento": "slow",
      "texto_overlay": "100% a tu medida",
      "texto_posicion": "bottom_center",
      "transicion_salida": "slide_left",
      "duracion_transicion": 0.5
    },
    {
      "numero": 3,
      "duracion": 7,
      "tipo": "visual_con_efectos",
      "prompt_imagen": "Cliente viendo el placar instalado, sonriendo",
      "efecto": "zoom_slow",
      "efecto_intensidad": "medium",
      "texto_overlay": "Diseñamos tu hogar",
      "cta": "Consultanos 👇",
      "transicion_salida": "fade",
      "duracion_transicion": 0.3
    },
    {
      "numero": 4,
      "duracion": 5,
      "tipo": "grafico_sticker",
      "contenido": "Texto CTA grande: 'Presupuesto sin compromiso'",
      "color_fondo": "#1A1816",
      "sticker_posicion": "bottom_center",
      "transicion_salida": "fade",
      "duracion_transicion": 0.3
    }
  ],
  "audio": {
    "tipo": "musica",
    "nombre": "Nombre canción",
    "duracion": 25,
    "volume": 80,
    "fade_in": 0.5,
    "fade_out": 0.5,
    "voz_en_off": false
  },
  "color_scheme": {
    "primario": "#1A1816",
    "secundario": "#F5F0EB",
    "acentos": "#C4A882"
  },
  "hashtags": ["#placar", "#mueblesamedida", "#diseño", "#hogar"],
  "cta_whatsapp": "1158018086",
  "watermark": true
}
```

**Esto se pasa a:**
- **Kling 2.5** (generar video de imagen estática)
- **CapCut** (edición manual si quieres full control)
- **Remotion** (edición AUTOMATIZADA con Claude Code) ← OPCIÓN NUEVA

---

## 🤖 FLUJO CON AGENTES (Propuesta Final)

```
┌──────────────────────────────────────────────────────────────────┐
│ LUNES 9AM — Lucas escribe IDEAS CRUDAS en Excel                  │
│ (título, formato, idea bruta, producto a destacar)               │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ AGENTE 1: CONTENT GENERATOR                                      │
│ Input: Hoja IDEAS CRUDAS (Lucas escribe 5 ideas)                │
│ Output: Completa hoja CLAUDE automáticamente:                   │
│   - Gancho perfeccionado                                         │
│   - Copy completo (guion + CTA)                                 │
│   - Prompt Imagen IA (para Nano Banana/Freepik)                │
│   - Prompt JSON (para Kling 2.5/CapCut/Remotion)               │
│   - Caption + hashtags                                          │
│   - Keyword SEO                                                 │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ LUNES 10AM — Lucas REVISA hoja CLAUDE                           │
│ (2-3 min por post, solo aprueba/rechaza)                        │
│ Si rechaza: especifica cambio → Agent regenara                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ LUCAS copia PROMPT IMAGEN → Nano Banana / Freepik              │
│ Espera imagen IA generada                                        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ OPCIÓN A: CapCut Manual                                          │
│ Lucas edita video con imagen IA (control creativo)             │
│                                                                  │
│ OPCIÓN B: AGENTE 2 (Remotion + Claude Code) — AUTOMATIZADO     │
│ Input: Video base + Prompt JSON                                │
│ Output: Video editado con:                                      │
│   - Texto overlay (del copy)                                   │
│   - Transiciones (según JSON)                                  │
│   - Timing sincronizado (duración exacta)                      │
│   - Watermark Polt Mobilier                                    │
│   - Export MP4 listo                                           │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ AGENTE 3: SCHEDULER + PUBLISHER                                  │
│ Publica automáticamente en horarios óptimos (9am, 6pm, 9pm)    │
│ Marca en CLAUDE como "Publicado"                               │
│ Guarda post_id de IG para tracking                            │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ SEMANA: AGENTE 4 (DM/Comment Responder)                        │
│ Responde automáticamente comentarios                            │
│ Flaggea preguntas complejas para Lucas                         │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ VIERNES 5PM — AGENTE 5 (Analytics)                             │
│ Genera hoja ANALYTICS con:                                      │
│   - Reach, Impressions, Engagement de cada post                │
│   - Conversiones (consultas, presupuestos, ventas)            │
│   - Ranking: mejor formato, mejor hora, mejor pilar           │
│   - Recomendaciones para próxima semana                        │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│ LUCAS LEE ANALYTICS (10 min)                                     │
│ Toma decisiones: ¿qué pilar publicar más? ¿qué hora?          │
│ Anota en CALENDARIO CONTENIDO para próxima semana              │
└──────────────────────────────────────────────────────────────────┘
```

---

## ⏱️ TIEMPO TOTAL (Con Agentes + Remotion)

| Tarea | Tiempo |
|-------|--------|
| Escribir IDEAS CRUDAS (5 ideas) | 10 min |
| Revisar/aprobar CLAUDE (Agent generó) | 10 min |
| Pasar PROMPT IMAGEN a Freepik (espera) | 15 min (paralelo) |
| Si es Reel: pasar video base a Remotion Agent | 5 min |
| Remotion Agent edita video automático | 5 min (paralelo) |
| Revisar/aprobar video editado | 5 min |
| **Total por semana (5 posts)** | **~50-60 min** |
| **Viernes: Revisar Analytics** | **10 min** |
| **TOTAL SEMANAL** | **~70 min (vs. 600 min manual)** |

**AHORRO: ~8.5 HORAS/SEMANA = 88% MENOS TIEMPO**

---

## 📊 COMPARACIÓN: Estructura Actual POLT vs. Propuesta

### Actual (incomplete):
- Tiene "Hoja 19" con 14 columnas pero sin estructura clara
- "TABLA PRINCIPAL" con solo 2 filas (nunca se usó)
- Sin hoja de IDEAS CRUDAS (no hay brainstorm tracking)
- Sin ANALYTICS (no mide qué funciona)
- Sin PROMPT JSON para video (proceso manual)

### Propuesta nueva:
✅ **Ideas Crudas** - Brainstorm inicial  
✅ **Claude** - Contenido base para agentes  
✅ **Calendario Contenido** - Vista semanal  
✅ **Analytics** - Tracking de métricas post-publicación  
✅ **PROMPT JSON** - Estructura para automación video  

---

## 🚀 IMPLEMENTACIÓN INMEDIATA

### **Paso 1: Hoy**
Creo nuevo Excel con estas 4 hojas, importo el contenido parcial que tienes en Polt.

### **Paso 2: Mañana**
Creo los 3 agentes:
1. **AGENTE CONTENT GENERATOR** — Genera CLAUDE automáticamente desde IDEAS CRUDAS
2. **AGENTE REMOTION VIDEO EDITOR** — Edita reels automáticamente (Remotion + Claude Code)
3. **AGENTE SCHEDULER** — Publica + trackea

### **Paso 3: Próxima semana**
Creo **AGENTE ANALYTICS** — Extrae métricas y sugiere optimizaciones.

---

## 💡 COLUMNAS NUEVAS que propongo AGREGAR

En la hoja **CLAUDE**, después de "PROMPT JSON":

| Nueva Columna | Tipo | Por qué |
|---------------|------|--------|
| **PERSONA OBJETIVO** | Dropdown | Pareja nido / Familia que renueva / Que remodela (tus 3 segmentos) |
| **DOLOR RESUELTO** | Dropdown | "Espacio no funciona" / "Nada encaja" / "Sin personalización" |
| **DIFERENCIAL DESTACADO** | Dropdown | A medida / Equipo integral / Flexible presupuesto / Restauración / Descuento efectivo |
| **PRODUCTO PRIMARIO** | Dropdown | Placar / Biblioteca / Escritorio / Restauración / General |
| **PRODUCTO SECUNDARIO** | Dropdown | Opcional, si se menciona otro |
| **PERSONA EN FOTO** | Dropdown | Sí / No / Avatar gráfico (para saber si buscar foto con persona o solo producto) |
| **ELEMENTO VISUAL CLAVE** | Texto | "Madera clara" / "Luz natural" / "Antes/después" (para briefs a fotógrafo/diseñador) |

---

*Propuesta lista. ¿Creo el Excel ahora con esta estructura?*
