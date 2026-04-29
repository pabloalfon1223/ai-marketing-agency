"""
Mente Pausada — Calendario Mayo 2026
PRUEBA: 1 post completo con todos los campos detallados
"""

MANYCHAT_TEMPLATE = "TRIGGERS: PAUSA / CALMA (misma respuesta automática para ambas palabras)\n\nMENSAJE:\nHola 🌙 Gracias por escribir.\n\nRuido Mental Cero es el protocolo de audio guiado de 7 noches que baja la activación mental cuando más la necesitás. Sin misticismo, sin postura de loto — solo técnica que funciona.\n\nAccedé acá 👉 [LINK]\n\n¿Preguntas? Respondé este mensaje 🙌"

POSTS = [
    {
        "falta": "Imágenes IA (Nano Banana) + Edición (Kling 2.5) + CapCut subtítulos",
        "formato": "Reel",
        "gancho": "POV: tu mente a las 2 AM elige este momento para procesar todo lo que salió mal",
        "etapa_buyer": "TOFU",
        "estado": "Idea",
        "guion": "REEL — 15 segundos (texto en pantalla, sin voz over)\n\n[0s-3s] Tu mente a las 2 AM:\n[3s-6s] ...el mensaje de hace 3 días que respondiste mal\n[6s-9s] ...la conversación que aún no tuviste\n[9s-12s] ...todo lo que tenés que hacer mañana\n[12s-15s] ...todo. a. la. vez.\n\n[Fade a negro]\n[Texto blanco grande]: Hay una forma de bajarlo. Escribí PAUSA.",
        "escenas": "ESCENA 1 (0s-3s): Plano cenital de cama deshecha en oscuridad total. Smartphone sobre sábanas mostrando 2:17 AM. Luz azul-blanca como única iluminación. Manos apenas visibles sin cara. Atmósfera: noche, tensión, insomnio.\n\nESCENA 2 (3s-12s): Fondo negro puro con partículas sutiles flotando. Cada línea de texto aparece con efecto typewriter. Textos anteriores se desvanecen.\n\nESCENA 3 (12s-15s): Vuelta al plano 1. Teléfono oscureciéndose (auto-lock). Sábanas muestran movimiento imperceptible. Habitación a negro total.",
        "audio": "Música: Lo-fi ambient cinético, 70-80 BPM. Estilo: sleepless thoughts lofi. Notas suaves de piano + strings minimalistas + vinilo grain suave. Volumen: 35-40%. Referencia: Epidemic Sound Night Thoughts Collection.",
        "caption": "tu mente a las 2 AM no necesita que la frenés con fuerza.\nnecesita que le des un lugar donde aterrizar.\n\nhay una técnica de 60 segundos que funciona exactamente para eso.\n\nescribí PAUSA y te cuento cómo.\n\n.\n..\n#mentepausada #ruidomental #ansiedad #insomnio #mindfulness #saludmental #bienestar #estres #calmarmente #dormirbien #mentalhealth #ansiedadnocturn #rutinarelajante #tecnicasderespiracion #autocuidado",
        "keyword": "PAUSA",
        "manychat": MANYCHAT_TEMPLATE,
        "prompts_json": [
            {
                "escena": 1,
                "duracion": "3s",
                "descripcion": "Cama deshecha de noche, teléfono con hora 2:17 AM, luz azul como única fuente",
                "nano_banana": "Cinematic top-down aerial shot of a completely disheveled bed with rumpled white cotton sheets and dark gray comforter in a pitch-black bedroom at night. A smartphone lies face-up on the right side of the bed displaying 2:17 AM in large white digits on the lock screen. The phone's cold blue-white backlight is the ONLY light source, creating deep shadows across the fabric wrinkles and casting a haunting glow. Male or female hands barely visible at the lower frame edge, blurred and featureless, no face in frame. Shallow depth of field with the phone slightly out of focus. Ultra-photorealistic cinematic grain. Color grading: cool blue tones from the phone contrasted with warm cream and gray textiles. Mood: insomnia, restlessness, midnight anxiety. 9:16 vertical format. Sony FX3 digital cinema camera aesthetic.",
                "kling_2_5_motion": "The phone screen flickers very subtly as if a notification is about to appear but does not. Tiny imperceptible breathing movement in the sheets. The bed fabric shows the faintest wrinkle shift as if someone just sighed. Camera completely locked, zero movement. Duration 3 seconds. Intensity: minimal, almost unperceptible."
            },
            {
                "escena": 2,
                "duracion": "9s",
                "descripcion": "Fondo negro puro con partículas sutiles flotando, texto apareciendo línea por línea",
                "nano_banana": "Pure jet black background (deep cinematic black, not pure #000000 but rich textured noir). Extremely subtle floating dust particles drifting slowly in random patterns, barely visible. Very fine film grain texture throughout (Kodak Portra 800 emulation). Minimalist, empty, contemplative. The background should feel like inner darkness. 9:16 vertical format. No other elements. Clean, dark, ready for text overlay.",
                "kling_2_5_motion": "Dust particles drift upward and sideways in slow random patterns. The grain texture pulses almost imperceptibly, like a breathing effect. Camera locked, zero movement. The movement is subtle enough to feel meditative rather than distracting. Duration 9 seconds."
            },
            {
                "escena": 3,
                "duracion": "3s",
                "descripcion": "Vuelta a cama, teléfono oscureciéndose, fade a negro total",
                "nano_banana": "Same aerial cinematic shot as Escena 1, but now the phone screen is dimming (auto-lock countdown at 50% brightness). The room is noticeably darker overall as if time has passed and darkness has deepened. The white sheets appear grayer, shadows more pronounced. The atmosphere is heavier, more resigned. The lighting is colder. Same photorealistic cinematic treatment as Escena 1.",
                "kling_2_5_motion": "The phone screen dims smoothly over 2 seconds (natural auto-lock fade). The rest of the room darkens simultaneously. The sheets show the barest imperceptible movement. Camera completely locked. Everything fades to black by the end. Duration 3 seconds. Intensity: slow, inevitable, like surrender."
            }
        ],
        "historias": "STORY 1: Poll vertical - Fondo índigo oscuro tipo cielo nocturno. Pregunta blanca grande: ¿Cuándo fue la última vez que tu mente se quedó en SILENCIO de verdad? Poll sticker: Esta semana vs Hace mucho. || STORY 2: Educativo - Fondo oscuro con luna suave. Texto: Tu mente no se callará sola a las 2 AM. / Pero podés darle un protocolo que funciona. / Nota: Respiración 4-7-8 baja cortisol en 60s. Link sticker: Saber más. || STORY 3: CTA - Fondo negro sólido con círculo de luz pulsando. Texto: Si querés bajarlo esta noche: Escribí PAUSA. / O mirá el post que subimos hoy."
    }
]
