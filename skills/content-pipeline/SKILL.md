---
name: content-pipeline
description: >
  Pipeline completo de contenido semanal: de ideas crudas a piezas listas para publicar.
  Úsalo cuando quieras generar el contenido de la semana, necesites 5-10 piezas
  de una vez, o quieras ejecutar el flujo de lunes (ideas → copy → brief visual → caption).
  Integra carrusel-designer y remotion-video. Aplica brand kits de los 3 proyectos.
  Basado en el sistema de 70 min/semana documentado para Polt Mobilier.
---

# SKILL: Content Pipeline

Ejecutás el pipeline completo de contenido semanal. De ideas crudas a piezas publicables.

## EL FLUJO COMPLETO

```
LUNES 9 AM
   ↓
[INPUT] 5 ideas crudas de Lucas
   ↓
[AGENTE 1] Content Generator
  → Hook perfeccionado
  → Copy completo (body + CTA)
  → Prompt imagen/video para IA
  → Caption + hashtags
   ↓
[LUCAS REVISA] — 15 minutos
  → ¿Aprueba? → Sigue
  → ¿Cambios? → Comentario → Regenera en 2 min
   ↓
[PRODUCCIÓN VISUAL]
  → Lucas copia prompt → Freepik/Gemini → imagen
  → Si reel: imagen → Kling 2.5 → video base
  → Si carrusel animado: usa SKILL remotion-video
   ↓
[AGENTE 2] Finalization
  → Adapta caption por plataforma (IG / TikTok / LinkedIn)
  → Sugiere mejor horario de publicación
  → Prepara para Buffer/Later si está configurado
   ↓
[OUTPUT] 5 piezas listas para publicar (Ma-Sa)
```

---

## PASO 1: RECIBIR IDEAS CRUDAS

Cuando Lucas diga "vamos con el pipeline" o "ideas de esta semana", pedí:

```
Dame las 5 ideas crudas de la semana para [proyecto]:
(pueden ser una frase, tema, o concepto sin desarrollar)

1. [idea cruda]
2. [idea cruda]
3. [idea cruda]
4. [idea cruda]
5. [idea cruda]
```

Si no tiene ideas, generá vos 5 basadas en:
- Pilares de contenido del proyecto
- Tendencias del momento
- Lo que más engagement tuvo antes

---

## PASO 2: GENERAR CONTENIDO (x5 ideas)

Para cada idea cruda, producí:

```
═══ PIEZA [N] — [DÍA] ═══
Idea cruda: [lo que dijo Lucas]
Formato: [Reel / Carrusel / Post único / Story]
Pilar: [pilar 1-6 según el proyecto]
Capa embudo: [TOFU / MOFU / BOFU]

HOOK:
[Primera línea/imagen que para el scroll]

COPY COMPLETO:
[Desarrollo 3-5 líneas]

CTA:
[Acción concreta]

PROMPT IMAGEN:
Herramienta: [Freepik / Gemini / Midjourney]
Prompt: [descripción detallada de la imagen]

CAPTION INSTAGRAM:
[Hook]

[Body]

[CTA + keyword ManyChat si aplica]

[hashtags]

HORARIO SUGERIDO: [día, hora óptima]
══════════════════════════════
```

---

## PASO 3: DISTRIBUCIÓN SEMANAL SUGERIDA

### MENTE PAUSADA (5 piezas/semana)
```
Martes: Pilar 1 (Micro-práctica) — Reel guiado [TOFU/MOFU]
Miércoles: Pilar 2 (Educación) — Carrusel [TOFU]
Jueves: Pilar 3 (Identidad) — Reel relatable [TOFU]
Viernes: Pilar 6 (Entretenimiento) — Reel divertido [TOFU]
Sábado: Pilar 5 (Conversión) — Con mención a RMC [BOFU]
```

### POLT MOBILIER (5 piezas/semana)
```
Lunes: Inspiración (antes/después, proyecto) — Post/Reel [TOFU]
Martes: Educativo (tips de diseño) — Carrusel [TOFU/MOFU]
Miércoles: Behind the scenes (proceso de fabricación) — Reel [MOFU]
Jueves: Testimonial (cliente satisfecho) — Post [MOFU/BOFU]
Viernes: Oferta suave (calculadora, consulta gratis) — Reel/Story [BOFU]
```

### CEREBRO (3 piezas/semana)
```
Lunes: Oportunidad de la semana — Post análisis
Miércoles: Framework/sistema — Carrusel educativo
Viernes: Caso de éxito — Post con datos
```

---

## PASO 4: ADAPTACIÓN POR PLATAFORMA

Para cada pieza, adaptá el caption según plataforma:

**Instagram:**
- Hook + 3-5 líneas + CTA + hashtags (15)
- Keyword ManyChat si aplica
- Emojis: moderados (2-3 por párrafo)

**TikTok:**
- Texto más corto, más directo
- Hashtags: 5-7 (más específicos)
- CTA: "Seguime para más"
- Stitch/Duet friendly si aplica

**LinkedIn** (si aplica para Cerebro):
- Tono más profesional
- Datos y cifras
- Sin hashtags de nicho, solo 3-5 amplios

---

## INTEGRACIÓN CON OTROS SKILLS

Si el formato es **carrusel** → activa `carrusel-designer`
```
→ Ir a SKILL carrusel-designer
→ Usar el copy de esta pieza
→ Diseñar slides completos
→ Generar briefs visuales por slide
```

Si el formato es **video animado** → activa `remotion-video`
```
→ Ir a SKILL remotion-video
→ Usar hook + copy + CTA de esta pieza
→ Generar código Remotion
→ Exportar MP4
```

Si necesitás **ads de la competencia** antes de crear → activa `competitive-ads`
```
→ Ir a SKILL competitive-ads
→ Analizar 5-10 anuncios del nicho
→ Extraer patterns
→ Volver al pipeline con insights
```

---

## OUTPUT FINAL DEL PIPELINE

```
═══ PLAN DE CONTENIDO SEMANAL ═══
Proyecto: [Proyecto]
Semana: [fecha]
Piezas: 5
Formatos: [breakdown]

MARTES: [título pieza 1]
MIÉRCOLES: [título pieza 2]
JUEVES: [título pieza 3]
VIERNES: [título pieza 4]
SÁBADO: [título pieza 5]

[Cada pieza desarrollada con hook, copy, prompt visual, caption]

TIEMPO ESTIMADO DE PRODUCCIÓN:
→ Generación (Claude): 5 min
→ Revisión (Lucas): 15 min
→ Producción visual: 30-45 min
→ TOTAL: ~1 hora para 5 piezas
══════════════════════════════════
```
