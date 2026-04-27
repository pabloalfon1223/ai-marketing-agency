# Mente Pausada — Departamento 1

**Estado:** 80% completado | **Prioridad:** 1

## Qué es
Producto digital de meditación y manejo del estrés. Ebook + audios guiados. Precios $99 / $149 / $199 USD.

## Estructura
```
mente-pausada/
├── landing/        ← Next.js + Stripe (PENDIENTE deploy)
├── emails/         ← Secuencias SendGrid día 0/3/7/10/14
├── ads/            ← Campañas Meta Ads (crear en PAUSED)
├── product/        ← Ebook + audios (assets)
└── plans/          ← Planes y estrategias
```

## Agentes que la sirven
- `content-director-mp` → Batch diario 10 piezas (7 AM ARG)
- `mp-scout` → Tendencias y competidores (manual)

Los prompts de agentes están en: `../ia-machine/agents/`
El sistema de contenido completo está en: `../ia-machine/agents/mente-pausada/`

## KPIs objetivo
- Revenue/mes: $3,000 USD
- Conversión: > 5%
- Ventas/día: 1-2

## Pendiente crítico
1. SendGrid API Key → activa triggers + emails
2. Deploy landing en Vercel
3. Primera venta orgánica → luego activar Meta Ads
