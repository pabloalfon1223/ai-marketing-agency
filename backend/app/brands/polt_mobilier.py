"""
Perfil de marca: Polt Mobilier Muebles
Configuracion completa para el sistema de agentes IA.
"""

BRAND_PROFILE = {
    "name": "Polt Mobilier Muebles",
    "industry": "Muebles a medida, diseno de interiores",
    "website": "www.poltmobiliermuebles.com.ar",

    "brand_voice": {
        "tono": "Aspiracional pero accesible, premium sin ser inalcanzable",
        "estilo": "Vocabulario de ambientes, espacios, hogar, cotidianidad bien vivida",
        "vocabulario": [
            "a medida", "tu espacio", "pensado para vos", "diseno",
            "funcionalidad", "hogar", "ambiente", "estilo", "personalizado",
            "calidad", "artesanal", "solucion", "habitar"
        ],
        "evitar": [
            "calidad insuperable", "los mejores precios", "no te lo pierdas",
            "ofertazo", "aprovecha", "vocabulario de ferreteria",
            "publicidad generica de muebleria masiva", "frases vacias"
        ]
    },

    "target_audience": {
        "perfil": [
            "Parejas equipando o renovando su primer hogar",
            "Familias que buscan funcionalidad + diseno",
            "Personas en proceso de reforma o remodelacion",
            "Gente que valora la personalizacion sobre lo masivo"
        ],
        "ubicacion": "Argentina",
        "dolor_principal": "No encuentro muebles que se adapten a MI espacio y MI estilo",
        "deseo": "Un hogar que funcione y se vea exactamente como lo imagine"
    },

    "differentials": [
        "Todo se fabrica a medida",
        "10% de descuento pagando en efectivo",
        "Servicio de restauracion de muebles",
        "Marca con estetica de diseno de interiores, no muebleria generica"
    ],

    "product_categories": [
        "Bibliotecas", "Camas", "Cunas", "Escritorios",
        "Placares/Vestidores", "Comodas/Cajoneras", "Estantes flotantes",
        "Mesas de luz", "Vanitorys", "Toalleros", "Alacenas",
        "Bajo mesadas", "Mesas", "Mesas de centro", "Racks",
        "Divanes", "Vajilleros", "Accesorios",
        "Muebles a medida (custom)", "Restauraciones"
    ],

    "channels": {
        "instagram": {
            "formatos": ["Post feed", "Carrusel", "Reel", "Story"],
            "frecuencia": "4-6 posts/semana",
            "mejor_horario": "9:00-11:00 AM y 7:00-9:00 PM (Argentina)"
        },
        "whatsapp": {
            "formatos": ["Difusion/catalogo", "Mensajes directos"],
            "uso": "Canal de venta directa, presupuestos, consultas"
        }
    },

    "visual_identity": {
        "estilo": "Fotos de ambientes reales, luz natural, espacios ordenados, estetica deco",
        "mood": "Hogar aspiracional, minimalismo calido, diseno escandinavo-argentino",
        "evitar_visual": "Fotos de catalogo generico, fondos blancos industriales, stockphotos"
    },

    "content_angles": [
        {"nombre": "Aspiracional", "descripcion": "Estetica, lifestyle, el hogar sonado"},
        {"nombre": "Funcional", "descripcion": "Solucion a problemas de espacio, orden"},
        {"nombre": "Emocional", "descripcion": "Hogar, familia, momentos cotidianos"},
        {"nombre": "Oferta", "descripcion": "Precio, descuento efectivo, promociones"}
    ],

    "cta_principales": [
        "Consultanos y te mandamos presupuesto sin compromiso",
        "Escribinos por WhatsApp",
        "Pedi tu presupuesto a medida",
        "Visita www.poltmobiliermuebles.com.ar"
    ]
}
