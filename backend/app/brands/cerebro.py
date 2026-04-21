"""
Perfil de marca: Cerebro
Sistema de ideacion y validacion de negocios escalables.
Configuracion completa para generador de ideas y validador de mercado.
"""

BRAND_PROFILE = {
    "name": "Cerebro",
    "industry": "Generacion de ingresos, innovation, idea validation",
    "website": None,

    "brand_voice": {
        "tono": "Analitico, practico, optimista, directo",
        "estilo": "Datos + intuicion. Que funciona, que no. Sin humo.",
        "vocabulario": [
            "oportunidad", "escalable", "MVP", "validacion", "demanda",
            "mercado", "tendencia", "viabilidad", "ingresos", "momentum",
            "experimento", "iteracion", "pivot", "potencial", "rentable"
        ],
        "evitar": [
            "garantizado", "te haras rico", "sin esfuerzo", "pasivo",
            "fantasias", "promesas sin datos", "hype sin base"
        ]
    },

    "objective": {
        "primario": "Identificar ideas de negocio con potencial real de $20k-50k/mes",
        "secundario": "Validar viabilidad antes de invertir tiempo/dinero",
        "filosofia": "Escalar progresivamente: $500/mes -> $2k -> $10k -> $20k+",
        "scope": [
            "SaaS y productos digitales",
            "Servicios y consultorias",
            "E-commerce y productos fisicos",
            "Creator economy y contenido",
            "Negocios hibridos y arbitrage"
        ]
    },

    "workflow": {
        "fase_1": "Generacion de ideas - 20+ ideas ranqueadas por escalabilidad",
        "fase_2": "Validacion rapida - demanda + competencia + score viabilidad",
        "fase_3": "Priorizacion - cuales explorar primero, MVP outline",
        "fase_4": "Tracking - historico de validaciones, learnings, pivots"
    },

    "validation_criteria": {
        "demanda": {
            "metrica": "Google Trends, Reddit, ProductHunt, TikTok searches",
            "peso": 40,
            "threshold": "Tendencia creciente o pico consistente en ultimos 6 meses"
        },
        "escalabilidad_a_20k": {
            "metrica": "Tiempo estimado a $20k/mes, capital requerido, complejidad",
            "peso": 40,
            "threshold": "Alcanzable en 6-12 meses con capital <$5k"
        },
        "competencia": {
            "metrica": "Numero de competidores, precio, gaps identificados",
            "peso": 20,
            "threshold": "Existe mercado pero hay espacio (no saturado, no inexistente)"
        }
    },

    "score_ranges": {
        "80_100": {
            "label": "ALTO POTENCIAL",
            "descripcion": "Explorar seriamente, validar MVP en 2-4 semanas"
        },
        "60_79": {
            "label": "POTENCIAL",
            "descripcion": "Vale la pena investigar mas, depende de capital/tiempo disponible"
        },
        "40_59": {
            "label": "POSIBLE",
            "descripcion": "Idea viable pero requiere validacion profunda o diferenciacion"
        },
        "0_39": {
            "label": "BAJO POTENCIAL",
            "descripcion": "Descartar o pivotear radicalmente"
        }
    },

    "tracking": {
        "estados": [
            "idea_cruda",           # Idea generada, sin revisar
            "en_validacion",        # Actualmente investigando
            "mvp_diseñado",         # MVP outline completado
            "mvp_en_desarrollo",    # Trabajando en MVP
            "mvp_validando",        # MVP en mercado, validando
            "track_a_20k",          # En proceso, camino a $20k/mes
            "exitosa",              # Alcanzó $20k/mes
            "pivotada",             # Se cambio direction
            "descartada"            # No viable
        ]
    },

    "content_strategy": {
        "semanal": "Trending ideas (lunes 8 AM): top 10 oportunidades del momento",
        "mensual": "Retrospective: que funciono, que no, proximas a explorar",
        "quarterly": "Strategy review: ajustar objetivo si es necesario"
    },

    "ethical_limits": [
        "NO garantizar ingresos ni exito",
        "Ser honesto sobre complejidad y tiempo requerido",
        "Señalar cuando una idea probable falle",
        "Datos antes que optimismo"
    ]
}
