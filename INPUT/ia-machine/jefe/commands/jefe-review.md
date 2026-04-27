Review semanal del sistema completo. Ejecutar viernes o cuando se pida.

Uso: /jefe-review [opcional: proyecto específico]

**PROCESO:**

1. LEE logs de la semana en:
   C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\ia-machine\shared\logs\

2. LEE state.json actual y compara con semana anterior si hay historial

3. ANALIZA por proyecto:
   **Mente Pausada:** revenue vs meta | ventas vs semana anterior | contenido generado | engagement estimado
   **Polt Mobilier:** leads nuevos | propuestas enviadas | cierres | ticket promedio
   **Cerebro:** oportunidades evaluadas | experimentos activos | hallazgos de valor

4. EVALÚA agentes:
   - ¿Cuáles tienen successRate < 90%?
   - ¿Algún prompt genera outputs de baja calidad?
   - ¿Hay tareas que tardaron demasiado?

5. PROPONE mejoras:
   - Máximo 3 mejoras concretas a prompts
   - Cada mejora incluye: agente, problema detectado, cambio propuesto, impacto esperado
   - Presentar como opciones para que Lucas apruebe o rechace

6. OUTPUT final:
```
📊 REVIEW SEMANAL — [fecha]

MÉTRICAS
━━━━━━━━━━━━━━
[tabla comparativa semana/semana]

AGENTES — PERFORMANCE
━━━━━━━━━━━━━━
[lista con semáforo 🟢🟡🔴]

MEJORAS PROPUESTAS
━━━━━━━━━━━━━━
1. [mejora concreta] → ¿Aprobás? (S/N)
2. [mejora concreta] → ¿Aprobás? (S/N)
3. [mejora concreta] → ¿Aprobás? (S/N)

PRÓXIMA SEMANA — FOCO
━━━━━━━━━━━━━━
[top 3 objetivos, ordenados por impacto en revenue]
```
