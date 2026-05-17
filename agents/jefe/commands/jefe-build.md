Constructor de apps, videos, carruseles y skills. El meta-comando que crea cosas nuevas.

Uso: /jefe-build [tipo] "[descripción]"

**TIPOS DISPONIBLES:**

**landing** → Landing page Next.js + Stripe
Ejemplo: /jefe-build landing "Mente Pausada — venta ebook meditación"
Proceso: 3 preguntas (producto, precio, audiencia) → genera Next.js completo → instrucciones deploy Vercel

**video** → Script + estructura Remotion para reel/TikTok
Ejemplo: /jefe-build video "reel MP 30s sobre cortisol nocturno"
Proceso: guion → estructura escenas → componentes Remotion → listo para renderizar

**carrusel** → 10 slides para Instagram
Ejemplo: /jefe-build carrusel "cómo elegir tu cocina Polt"  
Proceso: hook → 8 slides contenido → CTA → formato compatible open-carrusel

**skill** → Nueva skill custom para Claude Code
Ejemplo: /jefe-build skill "agente que responde reseñas de Google Maps"
Proceso: usa skill-creator → define objetivo + contexto + formato → genera .md listo

**app** → Aplicación completa (web, dashboard, herramienta)
Ejemplo: /jefe-build app "calculadora de presupuestos Polt web"
Proceso: blueprint primero (arquitectura, stack, páginas) → aprobación → construcción paso a paso

**email** → Secuencia de emails de marketing
Ejemplo: /jefe-build email "secuencia post-compra Mente Pausada"
Proceso: usa email-sequence skill → día 0/3/7/10/14 → HTML listo para SendGrid

**ads** → Copy para Meta Ads (Facebook/Instagram)
Ejemplo: /jefe-build ads "3 variantes para Mente Pausada $99"
Proceso: usa ad-creative + copywriting skills → primario/titular/descripción × 3 variantes → PAUSED

**REGLAS:**
- Siempre pedir confirmación del blueprint antes de construir apps grandes
- Videos y carruseles: generar estructura primero, renderizado después
- Ads: siempre incluir instrucción "crear en PAUSED, activar manualmente"
- Skills nuevas: guardar en ~/.claude/skills/ con nombre descriptivo
