Ejecutá un agente específico ahora mismo, de forma manual (sin esperar el trigger programado).

Uso: /jefe-run [nombre-agente]

**AGENTES DISPONIBLES:**
- content-director-mp → Content Director de Mente Pausada (genera batch diario de 10 piezas)
- polt-contenido → Contenido diario Polt Mobilier (posts + templates WhatsApp)
- cerebro-scanner → Market Scanner (análisis de oportunidades)
- daily-digest → Digest del día (top 3 acciones, estado general)
- daily-analytics → Analytics de los 3 proyectos (KPIs, tendencias)
- mp-scout → Scout de tendencias Mente Pausada
- polt-lead-scorer → Scorer de leads Polt Mobilier
- self-improver → Revisar y mejorar prompts de agentes

**PROCESO:**
1. Identifica el agente solicitado
2. Carga su prompt desde C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\ia-machine\agents\
3. Ejecuta con contexto completo del proyecto correspondiente
4. Guarda output en C:\Users\lucas\AppData\Roaming\Claude\CLAUDE\ia-machine\shared\logs\[agente]-[fecha].md
5. Actualiza state.json con lastRun y resultado
6. Muestra resumen del output

Si el agente no existe, lista los disponibles y pregunta cuál.
