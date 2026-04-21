"""
Perfil de marca: Mente Pausada
Configuracion completa para el sistema de agentes IA.
"""

BRAND_PROFILE = {
    "name": "Mente Pausada",
    "industry": "Bienestar, mindfulness, salud mental (no clinica), habitos",
    "website": None,

    "brand_voice": {
        "tono": "Calido, cercano, pausado, compasivo, practico",
        "estilo": "Como un amigo que sabe de bienestar y te habla sin tecnicismos",
        "vocabulario": [
            "pausar", "respirar", "soltar", "permiso", "ritmo",
            "calma", "habito", "momento", "cuerpo", "escuchar",
            "presente", "compasion", "alivio", "espacio", "cuidar"
        ],
        "evitar": [
            "cura", "elimina ansiedad", "diagnostico", "terapia reemplazada",
            "nunca mas vas a sentir", "solucion definitiva", "tecnicismos medicos",
            "lenguaje alarmista", "culpabilizador", "urgente/caotico"
        ],
        "disclaimer": "Esto no reemplaza terapia profesional"
    },

    "target_audience": {
        "edad": "20-45 anos",
        "perfil": [
            "Personas con estres/ansiedad cotidiana",
            "Profesionales con poco tiempo",
            "Gente que quiere habitos de calma",
            "Estudiantes",
            "Madres/padres",
            "Personas que 'no les sale meditar'"
        ],
        "ubicacion": "Argentina / LATAM",
        "dolor_principal": "Siento que no puedo parar, estoy siempre acelerado/a, no se como calmarme",
        "deseo": "Encontrar calma sin que sea complicado ni tome mucho tiempo"
    },

    "visual_identity": {
        "paleta": {
            "primarios": ["#E8DCC8", "#A8B5A0", "#F5F0E8"],
            "acentos": ["#7D8B75", "#D4C5A9", "#B8A88A"],
            "texto": ["#3D3D3D", "#5C5C5C"]
        },
        "estilo": "Luz calida, paleta de tierra/verde/crema, ritmo lento, espacios, tipografia simple y grande",
        "mood": "Minimalismo calido, naturaleza suave, amanecer, tazas de te, espacios ordenados",
        "tipografia": "Sans-serif simple y grande (Nunito, Quicksand, o similar)",
        "evitar_visual": "Nada de energia caotica, colores neon, movimientos rapidos, imagenes saturadas"
    },

    "content_pillars": [
        {
            "nombre": "Micro-practicas",
            "descripcion": "Regulacion: respiracion, grounding, cuerpo. Ejercicios de 1 minuto.",
            "porcentaje": 25
        },
        {
            "nombre": "Educacion simple",
            "descripcion": "Estres, rumiacion, sistema nervioso explicado sin tecnicismos",
            "porcentaje": 20
        },
        {
            "nombre": "Identidad y vinculo",
            "descripcion": "Historias, vulnerabilidad cuidada, 'me pasa lo mismo'",
            "porcentaje": 20
        },
        {
            "nombre": "Limites y autocuidado",
            "descripcion": "Decir que no, soltar, poner limites sin culpa",
            "porcentaje": 15
        },
        {
            "nombre": "Conversion suave",
            "descripcion": "Recursos, audios, sesiones - sin presion",
            "porcentaje": 10
        },
        {
            "nombre": "Entretenimiento que nutre",
            "descripcion": "Memes de bienestar, humor suave, relatable content",
            "porcentaje": 10
        }
    ],

    "channels": {
        "instagram": {
            "formatos": ["Reels", "Carruseles", "Stories", "B-Roll + frase"],
            "frecuencia": "5-7 posts/semana",
            "mejor_horario": "8:00-10:00 AM y 8:00-10:00 PM (Argentina)"
        },
        "tiktok": {
            "formatos": ["Videos cortos educativos", "POV", "Storytime"],
            "frecuencia": "3-5 videos/semana",
            "mejor_horario": "12:00-2:00 PM y 7:00-9:00 PM"
        },
        "youtube_shorts": {
            "formatos": ["Shorts de micro-practicas", "Tips rapidos"],
            "frecuencia": "2-3/semana",
            "mejor_horario": "10:00 AM"
        }
    },

    "ethical_limits": [
        "NO inventar credenciales ni avales medicos",
        "NO prometer 'cura', 'elimina ansiedad' ni diagnosticos",
        "Disclaimer cuando aplique: 'Esto no reemplaza terapia'",
        "Si aparece crisis/autolesion: derivar a profesional/urgencias",
        "Lenguaje: NUNCA alarmista ni culpabilizador"
    ],

    "content_workflow": {
        "fase_1": "Ideas crudas - 12 ideas: Hook + formato + idea rapida",
        "fase_2": "Guion IA-ready - Guion completo con escenas, texto en pantalla, visual",
        "fase_3": "Handoff prompts IA - Brief para generar con Midjourney/Runway/Kling"
    }
}
