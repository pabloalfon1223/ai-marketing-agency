"""
Polt Mobilier — Calendario Mayo 2026
PRUEBA: 1 post completo con todos los campos detallados
"""

MANYCHAT_TEMPLATE = "TRIGGERS: COTIZA / PRECIO (misma respuesta automática para ambas palabras)\n\nMENSAJE:\nHola! Gracias por escribir a Polt Mobilier.\n\nPara armarte una cotización personalizada, necesitamos saber:\nQué mueble tenés en mente? (placar, biblioteca, escritorio, etc)\nMedidas del espacio?\nMaterial o estilo preferido?\n\nRespondé con esos detalles y te enviamos el presupuesto sin compromiso."

POSTS = [
    {
        "falta": "Time-lapse taller (video grabado) + Kling 2.5 edición + CapCut transiciones",
        "formato": "Reel",
        "gancho": "Así queda un placar cuando lo hacemos a TUS medidas (antes y después en 20 segundos)",
        "etapa_buyer": "TOFU",
        "estado": "Idea",
        "guion": "REEL — 20 segundos (sin voz over, solo música y sonidos ambiente sutiles)\n\n[0s-2s] Plano general del taller vacío con paredes blancas y herramientas visibles\n[2s-8s] Time-lapse: carpintero midiendo, cortando madera, armando estructura (4x speed)\n[8s-14s] Time-lapse: lijado, lacado, instalación de herrajes (4x speed)\n[14s-18s] Transición suave: resultado final en el espacio del cliente\n[18s-20s] Placar TERMINADO e instalado. Persona (espalda, sin cara) admirando el resultado.\n\n[Texto final superpuesto]: De cero a placar. Solo para vos. COTIZA",
        "escenas": "ESCENA 1 (0s-2s): Plano general del taller Polt Mobilier. Piso hormigón industrial. Paredes blancas. Herramientas profesionales organizadas. Luz natural desde ventanas. Atmósfera: craftsmanship, precisión, calidad. Buenos Aires.\n\nESCENA 2 (2s-8s): Time-lapse del proceso. Carpenter mide madera, sierra corta tablones (polvo flotante), estructura armada en caballete, otro ángulo del proceso. Manos visibles sin cara. Ritmo productivo.\n\nESCENA 3 (8s-14s): Time-lapse de acabado final. Lijadora en acción, pintura aplicada, herrajes instalados, pulido final. Cada paso visible pero fluido.\n\nESCENA 4 (14s-18s): Transición a casa real. Antes: pared vacía (flash). Después: placar blanco minimalista instalado. Luz natural entra desde ventana. Transformación visible.\n\nESCENA 5 (18s-20s): Persona (female, back facing, sin cara) con brazo extendido tocando el placar, admirando. Movimiento lento satisfecho. Close-up del placar: líneas perfectas, acabado impecable.",
        "audio": "Música: Indie cinematic instrumental, 90-100 BPM. Estilo: craftsmanship/building vibes. Cello + piano minimalista + percusión suave. Volumen: 60%. Sonidos reales: sierra en segundo plano, lijadora suave, pincel aplicando laca (20% volumen). Referencia: Made by Hand tipo tracks en Epidemic Sound. Final con pequeño swell emocional.",
        "caption": "de cero a placar en 20 segundos.\n\nesto es lo que pasa en el taller de polt cuando alguien dice: necesito un placar que entre EXACTAMENTE aquí.\n\nmedidas precisas + madera de calidad + proceso artesanal = mueble que dura.\n\nnecsitás algo a medida? escribí COTIZA y empezamos.\n\n.\n..\n#poltmobilier #mueblesa medida #placara medida #diseñointerior #buenosaires #muebles #artesanía #diseñoargentino #hogar #dormitorio #espacios #interior #custom #craftsmanship #diseño",
        "keyword": "COTIZA",
        "manychat": MANYCHAT_TEMPLATE,
        "prompts_json": [
            {
                "escena": 1,
                "duracion": "2s",
                "descripcion": "Taller limpio y profesional, iluminación natural, herramientas organizadas",
                "nano_banana": "Wide establishing shot of a professional, industrial woodworking workshop in Buenos Aires (visible Argentine aesthetic). Clean polished concrete floor. White walls. Tall windows with abundant natural light flooding in. Professional woodworking tools hanging neatly on pegboards and walls: saws, sanders, clamps, measuring tapes. Large wooden workbenches with projects in progress. The space feels organized, trustworthy, artisanal. No people visible. The light is soft but bright, late afternoon golden hour. Color grade: warm whites, natural wood tones, industrial concrete grays. 9:16 vertical format. Photorealistic, cinematic, shallow depth of field. Sony FX3 cinema aesthetic.",
                "kling_2_5_motion": "Slow push-in from the wide shot toward the workbenches. Very slow, taking the full 2 seconds. Camera movement is steady and deliberate, revealing the professionalism. Dust particles float slowly in the light rays from the windows. No jerky movements. Intensity: slow, revealing, confidence-building."
            },
            {
                "escena": 2,
                "duracion": "6s",
                "descripcion": "Time-lapse del proceso de fabricación: medición, corte, armado, diferentes ángulos",
                "nano_banana": "Multiple shots in time-lapse (4x speed): 1) Close-up of carpenter hands measuring a wooden plank with metal tape measure. 2) Circular saw cutting through wood, sawdust particles floating in light rays. 3) Wooden frame structure assembled on workbench, C-clamps holding secure. 4) Wide shot of workbench with partially assembled cabinet frame. All shots in same workshop with natural window light. Hands visible, no face. Industrial but warm atmosphere. Each shot 1.5 seconds in time-lapse.",
                "kling_2_5_motion": "Time-lapse motion at 4x speed creates sense of productive work. Each shot transitions smoothly to the next. Camera angle changes slightly between shots (different angles of same workbench). No camera movement within each shot. Total duration 6 seconds playing at accelerated speed."
            },
            {
                "escena": 3,
                "duracion": "6s",
                "descripcion": "Time-lapse de acabado: lijado, lacado, herrajes, pulido final",
                "nano_banana": "Time-lapse shots (4x speed) of finishing work: 1) Electric sander smoothing wood surface, fine dust in air. 2) Close-up of brush applying white lacquer, smooth controlled strokes. 3) Installation of metal hinges and hardware on cabinet frame, hands positioning each piece precisely. 4) Final polishing step with cloth, surface becoming glossy and reflective. All shots show careful craftsmanship. Natural workshop light throughout. Warm, professional, artisanal. Each shot 1.5 seconds.",
                "kling_2_5_motion": "Time-lapse at 4x speed. Camera angles vary between shots. Close-ups of hands doing precise work, wider shots of cabinet. Accelerated motion creates sense of skilled, productive work. Smooth transitions between shots. Total 6 seconds at accelerated speed."
            },
            {
                "escena": 4,
                "duracion": "4s",
                "descripcion": "Transición: espacio vacío → placar instalado en dormitorio real, transformación antes/después",
                "nano_banana": "Shot 1 (1s): Empty bedroom wall - white, blank, empty space. Afternoon light from window to right. The wall is clean but bare. Shot 2 (3s): Same wall, same angle, but now a perfect white minimalist custom closet/cabinet is installed. Cabinet has clean lines, no handles, lacquered white finish reflecting light beautifully. Room is transformed - suddenly functional, beautiful, complete. Space feels more curated, more home. Afternoon light highlights cabinet's perfect finish. Color grade: warm whites, natural wood grain visible through lacquer, soft shadows.",
                "kling_2_5_motion": "Shot 1 has no motion, just empty space. Then smooth dissolve/fade transition (0.5s). Shot 2 begins and camera slowly pushes in toward cabinet (1.5s), revealing craftsmanship and perfect installation. Light catching the lacquered surface. Motion is slow, reverent, showing off quality."
            },
            {
                "escena": 5,
                "duracion": "2s",
                "descripcion": "Persona admirando el placar terminado, toque final, satisfacción",
                "nano_banana": "A woman (back facing camera, dark hair, no face visible) wearing casual home clothes stands in front of newly installed white lacquered cabinet. Right arm extended, hand gently touching cabinet surface. Posture relaxed, satisfied, admiring. Light from window illuminates both her and cabinet. Close-up on her hand touching smooth lacquered surface - quality visible in that contact. Room around her is clean, modern, complete. Color grade: warm, inviting, home-like. Shallow depth of field with focus on hand and cabinet surface.",
                "kling_2_5_motion": "Woman's arm reaches forward slowly over 1 second and gently touches cabinet. Hand lingers for a moment (0.5s). Then very slow pull-back from close-up (0.5s) revealing her satisfied posture. Motion is gentle, human, appreciative. No jerky movements. Gesture of admiration."
            }
        ],
        "historias": "STORY 1: Before/After Poll - Fondo blanco minimalista con imagen dividida en dos mitades. Izquierda: pared vacía blanca (antes). Derecha: placar blanco instalado (después). Pregunta: ¿Cuál es la transformación que más querés en tu casa? Poll: Espacio vacío vs Mueble a medida. || STORY 2: Education - Fondo texturizado tipo madera clara. Close-up de herraje acero inoxidable moderno. Texto: En Polt cada detalle importa. / Desde medidas exactas hasta herrajes que elegís vos. Link: Ver cómo hacemos. || STORY 3: CTA - Fondo blanco puro. Ícono/línea simple de placar. Texto: ¿Necesitás un mueble a medida? COTIZA gratis / O escribí PRECIO. Sticker CTA: Cotizar."
    }
]
