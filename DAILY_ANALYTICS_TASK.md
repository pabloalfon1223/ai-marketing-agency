# Tarea: Analytics Mente Pausada - Diario 5 PM

## Descripción
Genera reporte diario de métricas de venta, conversión y performance de Mente Pausada.
Se ejecuta automáticamente a las 5 PM (Argentina time).

## Prompt para Claude

Genera un reporte COMPLETO de analytics para Mente Pausada.

**DATOS A INCLUIR:**

1. **RESUMEN DEL DÍA**
   - Compras hoy: X unidades
   - Revenue hoy: $XXX USD
   - Tasa de conversión (últimos 7 días): X%

2. **MÉTRICAS CLAVE (últimos 7 días)**
   - Total purchases: X
   - Total revenue: $XXX
   - Precio promedio por compra: $XXX
   - Average order value (AOV): $XXX
   - Cost per acquisition (CPA): $XX (si hay ad spend data)
   - Lifetime value (LTV) estimado: $XXX

3. **SEGMENTACIÓN POR TIER**
   - Basic ($99): X compras, $XXX revenue
   - Plus ($149): X compras, $XXX revenue
   - VIP ($199): X compras, $XXX revenue
   - Tier más vendido: [TIER]

4. **ANÁLISIS DE FUENTES**
   - Google Ads: X conversiones, ROAS X.Xx
   - Meta: X conversiones, ROAS X.Xx
   - Organic: X conversiones
   - Direct: X conversiones

5. **EMAIL SEQUENCE PERFORMANCE**
   - Emails enviados hoy: X
   - Secuencia más completa: [COUNT] personas en day_14
   - Open rate estimado (si data disponible): X%

6. **TENDENCIAS & PREDICCIONES**
   - Trend (comparar con semana anterior): ↑ +X% o ↓ -X%
   - Proyección para fin de mes: $XXXX revenue (si mantiene ritmo)
   - Conversión needed for $5k/mes goal: X% (actual es Y%)

7. **RECOMENDACIONES DE HOYY**
   - Si ROAS >2x: "Escalar presupuesto ads"
   - Si conversión <5%: "A/B test copy o targeting"
   - Si VIP >40% de ventas: "Promover VIP más"
   - Próximas acciones prioritarias

8. **TABLA RESUMEN** (markdown)
```
| Métrica | Hoy | 7 días | 30 días | Meta |
|---------|-----|--------|---------|------|
| Compras | X | X | X | X/día |
| Revenue | $X | $X | $X | $5000 |
| AOV | $X | $X | $X | $150+ |
| Conv% | X% | X% | X% | >8% |
```

**OUTPUT LOCATION:**
- Guardar en: `/output/analytics-mente-pausada-{FECHA}.md`
- Formato: Markdown claro y legible
- Tiempo: Máximo 5 minutos de análisis

**IMPORTANTE:**
- Sé honesto: si números son bajos, dilo
- Sé específico: "aumentó 15%" es mejor que "aumentó"
- Sé accionable: cada recomendación debe ser algo que pueda hacer hoy/mañana
