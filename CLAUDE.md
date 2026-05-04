# AGENCIA IA — CLAUDE.md MAESTRO
> Este archivo es el punto de entrada de cada sesión. Leerlo completo antes de hacer cualquier cosa.

**Fecha última actualización:** 2026-05-03  
**Repositorio:** https://github.com/pabloalfon1223/ai-marketing-agency  
**Deploy activo:** https://ai-marketing-agency-ruby.vercel.app

---

## QUIÉNES SOMOS

Lucas (emprendedor) + Pablo (dev) construyendo una agencia de IA enfocada en LATAM.

**Objetivo final:** $10.000 USD/mes mediante productos digitales + servicios de automatización IA.  
**Filosofía:** Automatización primero. Todo lo que se puede automatizar, se automatiza. Siempre opción gratuita primero.  
**Idioma de trabajo:** Español

---

## PROYECTOS ACTIVOS

### 1. MENTE PAUSADA / RUIDO MENTAL CERO — PRIORIDAD 1
- **Producto:** Protocolo de 7 audios guiados para bienestar mental — $47 USD pago único
- **Estado:** 80% — faltan audios finales y deploy de landing
- **Checkout:** https://pay.hotmart.com/D103921572B (actualizar precio a $47)
- **Landing actual:** https://ruidomentalcero.lovable.app
- **Landing nueva:** `MENTE-PAUSADA/landing/index.html` → deploy en ruidomentalcero.com
- **Audios:** Script en `MENTE-PAUSADA/audios/generar_audios.py` (gTTS gratis)
- **Mercado:** Español global — México, Colombia, Chile, España, USA hispano (NO Argentina)
- **Paleta:** #1A1816 (cacao) · #F5EDD8 (cream) · #C4A882 (gold)
- **Bloqueadores:** Actualizar precio Hotmart · Generar 7 audios · Deploy landing

### 2. POLT MOBILIER — PRIORIDAD 2
- **Producto:** Muebles premium a medida — cocinas, placares, dormitorios
- **Mercado:** Buenos Aires y GBA — propietarios 30-50 años
- **Revenue actual:** $320k ARS/mes → Meta: $2M ARS/mes
- **Web:** https://poltmobiliermuebles.com.ar
- **CRM Sheets:** https://docs.google.com/spreadsheets/d/1h6pi9MBdvTnTCKU3FIsyXkeUiczjAkAVNEzYWfh1Vu4
- **Notificaciones CRM:** `POLT-MOBILIER/scripts/POLT_SHEETS_NOTIFICACIONES.js` (Google Apps Script)
- **Calculadora:** Polt Calculator Pro — expandir con módulo de cortes de madera
- **Pendiente:** Contenido automatizado (mismo sistema que Mente Pausada)

### 3. AGENCIA DE AUTOMATIZACIÓN IA — PRIORIDAD 3
- **Modelo:** Servicios de automatización IA para empresas ($800-3.000 USD/mes por cliente)
- **Primer cliente potencial:** Telmax — empresa de celulares, necesitan chatbot de calificación de leads
- **Servicios:** (1) Sistema de contenido IA · (2) CRM + automatizaciones · (3) Chatbot de ventas
- **Landing agencia:** ai-marketing-agency-ruby.vercel.app (vacía — rellenar)

### 4. CEREBRO — EN ESPERA
- **Objetivo:** Sistema de ideación continua para oportunidades $500+ USD/mes
- **Análisis hecho:** `CEREBRO/referencias/` — top oportunidades analizadas
- **Activar después de:** Mente Pausada generando ingreso

---

## HERRAMIENTAS Y STACK

| Área | Herramienta | Costo |
|---|---|---|
| Landing pages | Vercel + HTML/CSS | Gratis |
| Pagos | Hotmart | Comisión por venta |
| Emails | Resend.com | 3.000/mes gratis |
| Base de datos | Supabase | Gratis tier (ya configurado) |
| Imágenes | ChatGPT / Freepik / NanoBanana | Gratis |
| Videos | Kling 2.5 en Freepik | Gratis |
| Audio TTS | gTTS (Google) | Gratis sin límite |
| Contenido IA | AI Studio Gemini Flash | Gratis sin límite |
| Sheets | Google Sheets + Apps Script | Gratis |
| Control remoto | Claude en Slack | Ya instalado |

---

## WORKFLOW DE CONTENIDO

```
Idea cruda → AI Studio (gemini-flash, prompt maestro en /prompts/) 
→ JSON con guión + caption + hashtags + prompt_imagen + prompt_video
→ Imagen: ChatGPT o Freepik
→ Video: Kling 2.5 en Freepik
→ Publicar en Instagram / TikTok
```

Prompt maestro: `/prompts/PROMPT_MAESTRO_CONTENIDO.md` (dos versiones: Mente Pausada + Polt)

---

## PLUGINS DE CLAUDE CODE INSTALADOS

| Plugin | Función |
|---|---|
| `claude-ads` | Auditoría y optimización de Google/Meta/TikTok/LinkedIn Ads |
| `toprank` | SEO + GEO + Google Ads + Meta Ads con APIs |
| `uipro` (v2.2.3) | Creación y mejora de interfaces web |
| `caveman` | Respuestas comprimidas (~75% menos tokens) |
| `caveman-commit` | Commit messages comprimidos |

**Skills en `~/.claude/skills/`:**
- ia-machine: `carrusel-designer`, `content-pipeline`, `competitive-ads`, `landing-builder-pro`, `visual-prompt-generator`, `lead-scorer-polt`, `market-money-finder`, `monetization-orchestrator`, `audio-generator`, `remotion-video`, `obsidian-brain`
- marketing: `copywriting`, `email-sequence`, `social-content`, `page-cro`, `cold-email`, `launch-strategy`, `pricing-strategy`, `content-strategy`, `paid-ads`

---

## REGLAS DE TRABAJO

1. **Siempre opción gratuita primero.** Si hay opción paga mejor, mencionarla pero no como default.
2. **Todo lo que se hace, va al repo.** No crear archivos fuera de `ai-marketing-agency/`.
3. **Un proyecto a la vez.** Terminar Mente Pausada antes de escalar Polt. Escalar Polt antes de lanzar la agencia.
4. **Ser crítico.** Si algo no tiene sentido o hay una forma mejor, decirlo directamente.
5. **No usar palabras como:** "transformar", "journey", "empoderar", "sinergia" en copy de marca.

---

## ACCESO REMOTO

**Desde cualquier lugar:**
- Claude en Slack (ya instalado) → control por mensaje desde celular
- claude.ai/code → web app desde cualquier browser
- GitHub → todo el código y documentación accesible online

---

## CONTACTO / REPOSITORIOS

- GitHub principal: https://github.com/pabloalfon1223/ai-marketing-agency
- Supabase: xmdlrdhmydhtclqenjvf.supabase.co (ya configurado en settings.json)
- Hotmart: https://pay.hotmart.com/D103921572B
