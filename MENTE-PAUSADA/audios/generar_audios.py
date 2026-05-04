"""
GENERADOR DE AUDIOS — RUIDO MENTAL CERO
Usa ElevenLabs API (FREE tier: 10k chars/mes)
O Google TTS (gTTS) como fallback gratuito sin límite

OPCIONES DE VOCES (elegir una):
- ElevenLabs: "Rachel" (US neutral, calm) — más natural
- gTTS: es-MX, es-ES, es-CO — gratis, sin límite

INSTALAR:
  pip install gtts elevenlabs
"""

import os
from pathlib import Path

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────
METODO = "gtts"           # "gtts" (gratis) o "elevenlabs" (mejor calidad)
IDIOMA_GTTS = "es"        # es = español neutro
TLD_GTTS = "com.mx"       # com.mx = México | es = España | com = neutro
ELEVENLABS_KEY = ""        # Pegar API key de elevenlabs.io (free tier)
ELEVENLABS_VOICE = "Rachel"  # Rachel = neutral, calm en inglés | o usar voz en español
CARPETA_SALIDA = "audios"
# ──────────────────────────────────────────────────────────────────────

# Textos de los 7 audios (REEMPLAZAR con el contenido real del Google Doc)
AUDIOS = {
    "noche_1_el_primer_silencio.mp3": """
    Bienvenido. Esta noche es la primera.
    No necesitás hacer nada especial. Solo estar aquí, en esta cama, en este momento.
    Tu única tarea esta noche es escuchar.
    No importa si los pensamientos aparecen. Van a aparecer.
    Lo que cambia esta noche es que no tenés que seguirlos.
    Cerrá los ojos. Respirá. Estás aquí.
    """,

    "noche_2_respirar_diferente.mp3": """
    Segunda noche. Ya llegaste antes.
    Hoy vamos a trabajar con algo muy simple: tu respiración.
    Inhalá por la nariz durante cuatro tiempos.
    Uno. Dos. Tres. Cuatro.
    Retené dos tiempos.
    Y exhalá despacio por la boca durante seis.
    Uno. Dos. Tres. Cuatro. Cinco. Seis.
    Repetí ese ciclo. Tu sistema nervioso ya sabe qué hacer.
    """,

    "noche_3_soltar_el_dia.mp3": """
    Tercera noche. Antes de entrar en el descanso, hay algo que hacer.
    El día que pasó todavía está activo en tu mente.
    Vamos a cerrarlo conscientemente.
    Pensá en una cosa que hiciste hoy. Solo una.
    Reconocela. Y dejala ir.
    El día terminó. Lo que no se resolvió hoy puede esperar mañana.
    Esta noche, ya no hay nada por hacer.
    """,

    "noche_4_anclar_el_cuerpo.mp3": """
    Cuarta noche. Ya empezás a conocer este camino.
    Esta noche tu atención va a volver al cuerpo.
    Sentí el peso de tu cuerpo sobre la cama.
    Los puntos de contacto: los talones, la espalda, los hombros.
    Tu cuerpo ya sabe descansar. Solo necesita permiso.
    Dáselo.
    """,

    "noche_5_sin_agenda.mp3": """
    Quinta noche. Más de la mitad del camino.
    Esta noche hay algo que no tenés que resolver.
    Nada que planificar. Nada que revisar. Nada que preparar.
    La oscuridad no tiene agenda.
    La cama no te pide nada.
    El único trabajo de ahora es rendirse.
    """,

    "noche_6_el_cuerpo_primero.mp3": """
    Sexta noche. Casi al final.
    Hoy invertimos el orden. El cuerpo va primero.
    Empezá por los pies. Soltalos conscientemente.
    Las pantorrillas. Las rodillas. Los muslos.
    El abdomen. El pecho. Los hombros.
    Cuando el cuerpo descansa, la mente lo sigue.
    Siempre.
    """,

    "noche_7_ruido_mental_cero.mp3": """
    Séptima noche. Llegaste.
    Esta noche no hay nuevas instrucciones.
    Solo el silencio que construiste durante los últimos siete días.
    Ya sabés respirar diferente. Ya sabés soltar el día.
    Ya sabés anclar tu atención al cuerpo.
    Esta noche, todo eso se junta.
    Y el ruido... baja.
    Bienvenido al silencio.
    """,
}


def generar_con_gtts():
    from gtts import gTTS
    carpeta = Path(CARPETA_SALIDA)
    carpeta.mkdir(exist_ok=True)

    for nombre, texto in AUDIOS.items():
        texto_limpio = " ".join(texto.split())
        tts = gTTS(text=texto_limpio, lang=IDIOMA_GTTS, tld=TLD_GTTS, slow=False)
        ruta = carpeta / nombre
        tts.save(str(ruta))
        print(f"Generado: {ruta}")


def generar_con_elevenlabs():
    from elevenlabs import ElevenLabs, VoiceSettings
    client = ElevenLabs(api_key=ELEVENLABS_KEY)
    carpeta = Path(CARPETA_SALIDA)
    carpeta.mkdir(exist_ok=True)

    for nombre, texto in AUDIOS.items():
        texto_limpio = " ".join(texto.split())
        audio = client.text_to_speech.convert(
            text=texto_limpio,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel - calm, clear
            model_id="eleven_multilingual_v2",
            voice_settings=VoiceSettings(stability=0.75, similarity_boost=0.85, style=0.2)
        )
        ruta = carpeta / nombre
        with open(ruta, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        print(f"Generado: {ruta}")


if __name__ == "__main__":
    print(f"Generando audios con: {METODO}")
    if METODO == "gtts":
        try:
            import gtts
        except ImportError:
            print("Instalando gTTS...")
            os.system("pip install gtts")
        generar_con_gtts()
    elif METODO == "elevenlabs":
        if not ELEVENLABS_KEY:
            print("ERROR: Necesitás pegar tu API key de ElevenLabs en ELEVENLABS_KEY")
        else:
            generar_con_elevenlabs()
    print(f"\nListo. Audios guardados en carpeta '{CARPETA_SALIDA}/'")
    print("Subí esa carpeta a Google Drive o Cloudflare R2 y pegá los links en Hotmart.")
