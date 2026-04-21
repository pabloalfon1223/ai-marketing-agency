"""
Ads Strategy Agent for Mente Pausada
Generates ad copy, audience targeting, and budget recommendations
"""

ADS_STRATEGY_PROMPT = """Eres especialista en advertising para productos digitales y cursos.

TAREA: Generar estrategia completa de publicidad para Mente Pausada (ebook + audios).

CONTEXTO:
- Producto: Ebook + 25 audios sobre mindfulness, calma, hábitos
- Precio: $99-199 USD (3 opciones)
- Público: Personas 20-45, profesionales estresados, LATAM (especialmente Argentina)
- Presupuesto: $20-50/día (flexible)
- Plataformas: Meta (Facebook/Instagram) y Google Ads

ENTREGA:

1. **5 VARIANTES DE COPY** (emocional, racional, urgencia, social proof, aspiration)

Para CADA variante:
- Headline (max 30 chars)
- Primary text (max 125 chars)
- Description (max 30 chars)
- Hook visual (qué imagen/video describe)

Ejemplo formato:
---
VARIANTE 1: EMOCIONAL
Headline: "Calmate en 1 minuto"
Primary: "Respira profundo. Tu cuerpo necesita esto. Audios de calma que funcionan."
Description: "De personas como vos"
Hook: Persona respirando con ojos cerrados, luz cálida, ambiente tranquilo
---

2. **TARGETING POR PLATAFORMA**

META AUDIENCES (Facebook/Instagram):
- Audiencia 1: Interés "Meditation" + "Anxiety" + Income $50k+ = Profesionales
- Audiencia 2: Interés "Self-improvement" + "Wellness" + edad 30-45 = Lifestyle
- Audiencia 3: Lookalike de "high-value customers" = Expansion
- Audiencia 4: Retargeting website visitors = Warm audience

GOOGLE AUDIENCES:
- Keywords search: "anxiety relief", "meditation app", "calm techniques", "stress management"
- YouTube targeting: Channels sobre bienestar, meditación, productividad
- Display: Sites sobre salud mental, wellness, productividad

3. **BUDGET ALLOCATION** (diario)

Ejemplo para $30/día:
- Meta (70%): $21/día
  - Audiencia 1 (40%): $8.40
  - Audiencia 2 (35%): $7.35
  - Audiencia 3 (25%): $5.25
- Google (30%): $9/día
  - Search (60%): $5.40
  - YouTube (40%): $3.60

Rotación: Cambiar copy cada 3 días, audiences cada semana

4. **LANDING PAGE OPTIMIZATION TIPS**
- Headline must match ad promise (no bait-and-switch)
- Social proof (testimonials) visible above fold
- CTA (button) visible en viewport 1
- Mobile-first (80% traffic será mobile)
- Loading time <2 segundos

5. **TRACKING & METRICS**
- UTM parameters: utm_source=meta|google, utm_medium=cpc|display, utm_campaign=mente_pausada_basic|plus|vip
- Track: CTR, CPC, conversion rate, ROAS, LTV
- Winning copy: Si CTR >3%, CPC <$2, conversion >8%, scale up

6. **ESCALAMIENTO**
- Si ROAS >3x en week 1: Duplica presupuesto
- Si ROAS 1.5-3x: Mantén, optimiza copy
- Si ROAS <1.5x: Pausa, cambia targeting o copy
"""

def get_ads_strategy_prompt() -> str:
    return ADS_STRATEGY_PROMPT
