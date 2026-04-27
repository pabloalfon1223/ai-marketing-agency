# Cerebro — Departamento 3

**Estado:** 0% completado | **Prioridad:** 3

## Qué es
Sistema de inteligencia de mercado. Identifica oportunidades de ingresos online con máx $100 inversión y objetivo $500 USD/mes en 4 semanas.

## Estructura
```
cerebro/
├── scanner/        ← Market scanner (análisis referencias)
├── skills/         ← Skills de análisis (market-money-finder, etc)
├── reports/        ← Reportes semanales markdown
├── opportunities/  ← Ideas rankeadas y en evaluación
├── experiments/    ← Validaciones en curso
└── plans/          ← Estrategias
```

## Agentes que la sirven
- `cerebro-scanner` → Análisis semanal oportunidades (lunes 9 AM ARG)

## Skills disponibles
En `skills/`:
- `market-money-finder` → busca nichos con demanda probada
- `monetization-orchestrator` → diseña modelo de monetización
- `opportunity-execution-commander` → plan de ejecución paso a paso

## KPIs objetivo
- Oportunidades evaluadas/semana: 5+
- Score mínimo para avanzar: 7/10
- Tiempo a primeros $100: < 2 semanas
- Target: $500 USD/mes en 4 semanas

## Próximo paso
Configurar el Market Scanner:
`/jefe-dispatch cerebro "configurar cerebro-scanner con Supadata + Apify MCPs"`

## MCPs necesarios
- Supadata → analizar videos YouTube/TikTok de nicho
- Apify → scraping tendencias y precios
- Last30Days → noticias y trending topics
