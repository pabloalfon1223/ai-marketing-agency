"""
utils.py — Funciones auxiliares del sistema Mente Pausada
"""

import os
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


def load_agent_prompt(agent_name: str) -> str:
    """Carga el prompt de un agente desde el directorio agents/"""
    agent_path = ROOT_DIR / "agents" / f"{agent_name}.md"
    
    if not agent_path.exists():
        raise FileNotFoundError(f"Agente no encontrado: {agent_path}")
    
    with open(agent_path, "r", encoding="utf-8") as f:
        return f.read()


def load_config(config_name: str) -> dict:
    """Carga un archivo de configuración JSON."""
    import json
    config_path = ROOT_DIR / "config" / config_name
    
    if not config_path.exists():
        raise FileNotFoundError(f"Config no encontrado: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_brand_kit() -> str:
    """Carga el brand kit como texto."""
    brand_path = ROOT_DIR / "config" / "brand_kit.md"
    with open(brand_path, "r", encoding="utf-8") as f:
        return f.read()


def load_visual_categories() -> str:
    """Carga el sistema de categorías visuales."""
    cat_path = ROOT_DIR / "config" / "visual_categories.md"
    with open(cat_path, "r", encoding="utf-8") as f:
        return f.read()


def print_banner():
    """Imprime el banner del sistema."""
    print("\n" + "="*60)
    print("  🧠 MENTE PAUSADA — Sistema de Contenido Automatizado")
    print("  Versión 1.0 | Powered by Claude")
    print("="*60)


def print_step(message: str):
    """Imprime un paso del proceso."""
    print(f"\n→ {message}")


def print_success(message: str):
    """Imprime un mensaje de éxito."""
    print(f"  ✅ {message}")


def print_error(message: str):
    """Imprime un mensaje de error."""
    print(f"  ❌ {message}")


def validate_env():
    """Verifica que las variables de entorno necesarias están configuradas."""
    required = ["ANTHROPIC_API_KEY", "GOOGLE_SHEET_ID"]
    missing = []
    
    for var in required:
        value = os.getenv(var)
        if not value or value.endswith("COMPLETAR"):
            missing.append(var)
    
    if missing:
        print_error(f"Variables de entorno faltantes en .env: {', '.join(missing)}")
        print("  Seguí el SETUP.md para configurarlas.")
        return False
    
    return True


def format_json_for_display(data: dict, max_chars: int = 200) -> str:
    """Formatea un dict para mostrar en consola de forma legible."""
    import json
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text
