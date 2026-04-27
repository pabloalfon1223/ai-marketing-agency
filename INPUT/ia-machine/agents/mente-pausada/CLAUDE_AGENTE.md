# CLAUDE.md — Instrucciones para Claude Code

Este archivo le dice a Claude Code cómo operar en este proyecto.

## Contexto del proyecto

Este es el sistema automatizado de generación de contenido para **Mente Pausada**,
una marca de bienestar en español. El sistema genera fichas completas de producción
de contenido para Instagram y TikTok.

## Cómo ejecutar el sistema

```bash
# Generar una pieza
python scripts/generate_content.py --hook "GANCHO AQUI" --tipo Reel --etapa TOFU --keyword PAUSA

# Modo interactivo
python scripts/generate_content.py --interactive

# Verificar instalación
python scripts/generate_content.py --test

# Generar semana completa (5 piezas)
python scripts/generate_content.py --batch semana --cantidad 5
```

## Archivos críticos

- `config/brand_kit.md` — Identidad de marca, paleta, vocabulario, reglas
- `config/visual_categories.md` — Sistema A-H de variación visual
- `config/sheet_config.json` — Columnas del Google Sheet
- `agents/*.md` — Prompts de los 5 agentes del pipeline
- `scripts/generate_content.py` — Script principal
- `.env` — Credenciales (NO commitear a git)

## Pipeline de agentes

1. **scout_agent** → Lee el Sheet, detecta patrones repetidos
2. **guion_agent** → Genera guion + escenas + audio
3. **prompt_agent** → Genera prompts Flux (imagen) + Kling (video)
4. **copy_agent** → Genera caption + hashtags + ManyChat
5. **stories_agent** → Genera historias de Instagram

## Modificar comportamiento

Para cambiar qué genera cada agente: editar el archivo `.md` correspondiente en `agents/`.
Para cambiar la paleta o vocabulario: editar `config/brand_kit.md`.
Para cambiar la variación visual: editar `config/visual_categories.md`.

## Instalar dependencias

```bash
pip install anthropic google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
```

## Estructura del Google Sheet (columnas A-M)

A: Número | B: Formato | C: Hook | D: Etapa Buyer | E: Estado
F: Guion/Slides | G: Escenas detalladas | H: Audio/Sonido
I: Caption+Hashtags | J: Keyword | K: ManyChat | L: Prompt JSON | M: Historias

## Variables de entorno necesarias

Ver `.env.example` para la lista completa.
