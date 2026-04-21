---
name: obsidian-brain
description: >
  Sistema de memoria y documentación para el proyecto. Guarda aprendizajes,
  métricas, ideas y decisiones de forma organizada. Úsalo cuando quieras
  documentar algo importante, guardar un learning de una campaña, registrar
  métricas semanales, o recuperar información de sesiones anteriores.
  Basado en claude-obsidian de AgriciDaniel.
---

# SKILL: Obsidian Brain (Memoria del Sistema)

Sos el sistema de memoria del venture. Documentás todo lo que funciona,
lo que no funciona, y por qué. Sin memoria, repetimos errores.

## QUÉ DOCUMENTA ESTE SKILL

### CATEGORÍAS DE MEMORIA

```
/memory/
├── learnings/          ← Qué funcionó, qué no, por qué
├── metrics/            ← Métricas semanales/mensuales
├── ideas/              ← Ideas para probar (sin validar)
├── campaigns/          ← Campañas activas y sus resultados
├── content-winners/    ← Piezas de contenido que pegaron fuerte
└── decisions/          ← Decisiones estratégicas importantes
```

---

## FORMATO DE DOCUMENTACIÓN

### LEARNING (cuando algo resulta)
```markdown
# LEARNING — [fecha]
**Proyecto:** [Mente Pausada / Polt / Cerebro]
**Categoría:** [Contenido / Ads / Email / Producto / Operaciones]

## Qué pasó
[Descripción breve de la situación]

## Resultado
[Qué ocurrió — número, métrica, observación]

## Por qué funcionó / no funcionó
[Análisis de causa]

## Qué hacer diferente
[Cambio concreto a aplicar]

## Aplicar a:
- [ ] Mente Pausada
- [ ] Polt Mobilier  
- [ ] Cerebro

**Tags:** #contenido #hook #conversion #[otras]
```

---

### MÉTRICA SEMANAL
```markdown
# MÉTRICAS — Semana [N] / [fecha]

## MENTE PAUSADA
- Seguidores: [N] (+/- vs semana anterior)
- Alcance promedio: [N]
- Engagement rate: [%]
- DMs con "PAUSA": [N]
- Ventas: [N] ($[total])
- Email open rate: [%]

## POLT MOBILIER
- Seguidores: [N]
- Consultas recibidas: [N]
- Presupuestos enviados: [N]
- Órdenes cerradas: [N] ($[total])
- Tiempo promedio de cierre: [días]

## CEREBRO
- Ideas nuevas: [N]
- Ideas validadas: [N]
- Ideas descartadas: [N]
- Mejor idea de la semana: [nombre]
- Score promedio: [N/100]

## HIGHLIGHT DE LA SEMANA
[La cosa más importante que pasó]

## ACCIÓN PARA PRÓXIMA SEMANA
[Una cosa concreta a cambiar o probar]
```

---

### CONTENT WINNER
```markdown
# CONTENT WINNER — [nombre de la pieza]
**Fecha:** [cuando se publicó]
**Proyecto:** [proyecto]
**Formato:** [Reel / Carrusel / Post]
**Pilar:** [pilar de contenido]

## Métricas
- Alcance: [N]
- Engagement: [%]
- Guardados: [N]
- Comentarios: [N]
- DMs generados: [N]
- Ventas atribuibles: [N]

## Por qué pegó
[Análisis del hook / formato / timing]

## Cómo replicarlo
[Template o patrón a repetir]

## Variaciones a probar
1. [variación 1]
2. [variación 2]
```

---

## COMANDOS DE USO

Cuando el usuario diga:
- "guardá este learning" → documentar con formato LEARNING
- "métricas de la semana" → llenar formato MÉTRICA
- "este post pegó bien" → documentar como CONTENT WINNER
- "qué funcionó en emails" → buscar en /learnings con filtro email
- "retrospectiva del mes" → compilar todas las métricas + learnings del mes

---

## RETROSPECTIVA MENSUAL (primer día del mes)

```markdown
# RETROSPECTIVA — [Mes Año]

## LO QUE FUNCIONÓ
1. [cosa que funcionó + por qué]
2. [...]

## LO QUE NO FUNCIONÓ  
1. [cosa que falló + causa raíz]
2. [...]

## MÉTRICAS DEL MES
[Resumen de las 4 semanas]

## TOP 3 LEARNINGS DEL MES
1. [learning más valioso]
2. [...]
3. [...]

## DECISIONES PARA EL MES SIGUIENTE
1. [decisión concreta]
2. [...]
3. [...]

## PROYECCIÓN
- ¿En track para el objetivo?
- ¿Qué ajustar?
```
