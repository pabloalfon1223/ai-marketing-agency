# Polt Mobilier — Departamento 2

**Estado:** 50% completado | **Prioridad:** 2

## Qué es
Empresa de muebles a medida de alta gama, Argentina. Ticket promedio $250k-$450k ARS. Proceso: lead → cotización → propuesta → cierre.

## Estructura
```
polt-mobilier/
├── calculator/     ← Polt Calculator Pro (HTML ya existente, web app pendiente)
├── whatsapp/       ← WhatsApp AgentKit (PENDIENTE instalar)
├── leads/          ← Pipeline + scoring automático
├── marketing/      ← Contenido Instagram + templates
├── docs/           ← Docs de sistema y brand
└── plans/          ← Planes y estrategias
```

## Calculator Pro
Ya existe como HTML en `calculator/`. La versión web Next.js está pendiente:
`/jefe-build app "Polt Calculator Pro — versión web con guardado de presupuestos"`

## Agentes que la sirven
- `polt-contenido` → Posts + templates WhatsApp (9 AM ARG)
- `polt-lead-scorer` → Califica leads entrantes (automático)

## KPIs objetivo
- Leads/mes: 20+
- Tasa de propuesta: > 60% de leads calificados
- Cierre: > 30% de propuestas
- Revenue/mes: $2M ARS+

## Pendiente crítico
1. Instalar WhatsApp bot (Whapi.cloud free)
2. Pipeline digital de leads funcionando
3. Polt Calculator Pro web con Vercel
