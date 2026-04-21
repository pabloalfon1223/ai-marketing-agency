"""
Script de generacion diaria de 10 ideas de contenido listas para publicar.
Ejecutado automaticamente por Claude Code como tarea programada.
"""
import json
from datetime import datetime

# Template de contenido diario
CONTENT_PROMPT = """Genera exactamente 10 piezas de contenido COMPLETAMENTE listas para publicar hoy.

Para CADA pieza de contenido incluye:

1. **Titulo/Hook** - El titulo o gancho principal
2. **Plataforma** - Instagram, LinkedIn, Twitter/X, TikTok, Blog, Email
3. **Tipo** - Carrusel, Reel/Video, Post estatico, Story, Hilo, Articulo
4. **Texto completo** - El copy EXACTO listo para copiar y pegar, incluyendo emojis si aplica
5. **Hashtags** - 10-15 hashtags relevantes
6. **Call to Action** - La accion que queremos del usuario
7. **Horario sugerido** - Mejor hora para publicar
8. **Descripcion visual** - Que imagen/video/diseno acompana el post
9. **Formato** - Dimensiones y especificaciones tecnicas

Distribuye las 10 piezas asi:
- 3 para Instagram (1 carrusel, 1 reel, 1 story)
- 2 para LinkedIn (1 post, 1 articulo corto)
- 2 para Twitter/X (1 hilo, 1 post)
- 1 para TikTok (guion de video)
- 1 para Blog (articulo completo)
- 1 para Email (newsletter)

Temáticas variadas: educativo, inspiracional, detras de escena, caso de estudio,
tendencias, tips practicos, engagement/pregunta, promocional sutil.

IMPORTANTE: Todo el contenido debe estar 100% listo para copiar, pegar y publicar.
No dejes espacios en blanco ni [completar]. Todo terminado.
"""


def get_daily_prompt(client_info: dict | None = None) -> str:
    """Construye el prompt diario con contexto del cliente si existe."""
    today = datetime.now().strftime("%A %d de %B, %Y")
    prompt = f"Fecha: {today}\n\n"

    if client_info:
        prompt += f"Cliente: {client_info.get('name', 'General')}\n"
        prompt += f"Industria: {client_info.get('industry', 'General')}\n"
        if client_info.get('brand_voice'):
            prompt += f"Voz de marca: {client_info['brand_voice']}\n"
        if client_info.get('target_audience'):
            prompt += f"Audiencia objetivo: {client_info['target_audience']}\n"
        prompt += "\n"

    prompt += CONTENT_PROMPT
    return prompt


# Formato de salida esperado para cada pieza
CONTENT_SCHEMA = {
    "pieces": [
        {
            "number": 1,
            "title": "string",
            "platform": "instagram|linkedin|twitter|tiktok|blog|email",
            "post_type": "carrusel|reel|story|post|hilo|articulo|video|newsletter",
            "full_text": "string - texto completo listo para publicar",
            "hashtags": ["string"],
            "call_to_action": "string",
            "suggested_time": "string - ej: 9:00 AM",
            "visual_description": "string - descripcion de la imagen/video",
            "format_specs": "string - dimensiones y specs",
            "theme": "educativo|inspiracional|behind_scenes|caso_estudio|tendencias|tips|engagement|promocional"
        }
    ]
}
