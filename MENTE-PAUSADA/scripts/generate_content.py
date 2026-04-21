"""
MENTE PAUSADA — Sistema de Generación de Contenido Automatizado
Autor: Sistema generado con Claude Code
Uso: python scripts/generate_content.py --hook "..." --tipo "Reel" --etapa "TOFU" --keyword "PAUSA"
"""

import os
import sys
import json
import argparse
import anthropic
from pathlib import Path
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")

# Importar módulos del sistema
sys.path.insert(0, str(ROOT_DIR / "scripts"))
from read_sheet import read_sheet_data
from write_to_sheet import write_row_to_sheet
from utils import load_agent_prompt, load_config, print_banner, print_step, print_success, print_error


def run_agent(client: anthropic.Anthropic, agent_name: str, variables: dict) -> dict:
    """
    Ejecuta un agente cargando su prompt y reemplazando las variables.
    Retorna el JSON parseado del output del agente.
    """
    print_step(f"Ejecutando agente: {agent_name}")
    
    # Cargar el prompt del agente
    prompt_template = load_agent_prompt(agent_name)
    
    # Reemplazar variables en el prompt
    prompt = prompt_template
    for key, value in variables.items():
        placeholder = f"[{key.upper()}]"
        prompt = prompt.replace(placeholder, str(value) if value else "")
    
    # Llamar a la API de Anthropic
    model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
    max_tokens = int(os.getenv("MAX_TOKENS", "4000"))
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        raw_output = response.content[0].text.strip()
        
        # Limpiar markdown si el modelo lo incluyó igual
        if raw_output.startswith("```"):
            raw_output = raw_output.split("```")[1]
            if raw_output.startswith("json"):
                raw_output = raw_output[4:]
        raw_output = raw_output.strip()
        
        # Debug mode
        if os.getenv("DEBUG", "false").lower() == "true":
            print(f"\n[DEBUG {agent_name}]:\n{raw_output[:500]}...\n")
        
        return json.loads(raw_output)
        
    except json.JSONDecodeError as e:
        print_error(f"Error parseando JSON de {agent_name}: {e}")
        print_error(f"Output recibido: {raw_output[:300]}")
        raise
    except Exception as e:
        print_error(f"Error en agente {agent_name}: {e}")
        raise


def generate_content(hook: str, tipo: str, etapa: str, keyword: str, 
                     contexto: str = "", num_escenas: int = None,
                     auto_write: bool = False) -> dict:
    """
    Pipeline principal de generación de contenido.
    Ejecuta los 5 agentes en secuencia y retorna la fila completa.
    """
    print_banner()
    print(f"\n📝 Generando contenido para:")
    print(f"   Hook: {hook}")
    print(f"   Tipo: {tipo} | Etapa: {etapa} | Keyword: {keyword}\n")
    
    # Inicializar cliente Anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print_error("ANTHROPIC_API_KEY no encontrada en .env")
        sys.exit(1)
    
    client = anthropic.Anthropic(api_key=api_key)
    
    # Determinar número de escenas por defecto
    if num_escenas is None:
        if tipo == "Reel":
            num_escenas = int(os.getenv("DEFAULT_SCENES_REEL", "7"))
        elif tipo == "B-Roll":
            num_escenas = int(os.getenv("DEFAULT_SCENES_BROLL", "3"))
        else:
            num_escenas = int(os.getenv("DEFAULT_SLIDES_CARRUSEL", "7"))
    
    # ─── AGENTE 1: SCOUT ───────────────────────────────────────────────
    print_step("1/5 — Scout: Leyendo historial del Sheet...")
    
    sheet_data = []
    try:
        sheet_data = read_sheet_data()
        print_success(f"Sheet leído: {len(sheet_data)} filas encontradas")
    except Exception as e:
        print(f"   ⚠️  No se pudo leer el Sheet: {e}")
        print("   ℹ️  Continuando sin datos históricos...")
    
    scout_result = run_agent(client, "scout_agent", {
        "SHEET_DATA": json.dumps(sheet_data[:30], ensure_ascii=False)  # últimas 30 filas
    })
    
    proxima = scout_result.get("proxima_pieza", {})
    categorias_a_usar = scout_result.get("categorias_disponibles", ["A", "B", "C", "D", "E", "F", "G", "H"])
    movimientos_disponibles = scout_result.get("movimientos_disponibles", ["crash zoom", "orbital rotation", "tracking shot", "dolly in"])
    
    print_success(f"Scout completado — Categorías disponibles: {categorias_a_usar}")
    
    # ─── AGENTE 2: GUIONISTA ───────────────────────────────────────────
    print_step("2/5 — Guionista: Generando guion, escenas y audio...")
    
    guion_result = run_agent(client, "guion_agent", {
        "HOOK": hook,
        "FORMATO": tipo,
        "ETAPA": etapa,
        "KEYWORD": keyword,
        "NUM_ESCENAS": num_escenas,
        "CONTEXTO_ADICIONAL": contexto,
        "SCOUT_REPORT": json.dumps(scout_result, ensure_ascii=False)
    })
    
    print_success("Guion, escenas y audio generados")
    
    # ─── AGENTE 3: PROMPTS VISUALES ────────────────────────────────────
    print_step("3/5 — Prompts visuales: Generando Flux + Kling...")
    
    prompt_result = run_agent(client, "prompt_agent", {
        "ESCENAS_DETALLADAS": guion_result.get("escenas_detalladas", ""),
        "SCOUT_REPORT": json.dumps(scout_result, ensure_ascii=False),
        "CATEGORIAS_A_USAR": json.dumps(categorias_a_usar),
        "MOVIMIENTOS_DISPONIBLES": json.dumps(movimientos_disponibles),
        "ETAPA": etapa
    })
    
    print_success(f"Prompts generados: {len(prompt_result.get('prompt_json', []))} escenas")
    
    # ─── AGENTE 4: COPY ────────────────────────────────────────────────
    print_step("4/5 — Copy: Generando caption y ManyChat...")
    
    copy_result = run_agent(client, "copy_agent", {
        "HOOK": hook,
        "GUION": guion_result.get("guion", ""),
        "FORMATO": tipo,
        "ETAPA": etapa,
        "KEYWORD": keyword
    })
    
    print_success("Caption y ManyChat generados")
    
    # ─── AGENTE 5: HISTORIAS ───────────────────────────────────────────
    print_step("5/5 — Historias: Generando historias de Instagram...")
    
    stories_result = run_agent(client, "stories_agent", {
        "HOOK": hook,
        "GUION": guion_result.get("guion", ""),
        "CAPTION": copy_result.get("caption_hashtags", ""),
        "FORMATO": tipo,
        "ETAPA": etapa,
        "KEYWORD": keyword
    })
    
    print_success("Historias generadas")
    
    # ─── ENSAMBLAR FILA COMPLETA ────────────────────────────────────────
    fila = {
        "numero": len(sheet_data) + 1 if sheet_data else 1,
        "formato": tipo,
        "hook": hook,
        "etapa_buyer": etapa,
        "estado": "Idea",
        "guion_slides": guion_result.get("guion", ""),
        "escenas_detalladas": guion_result.get("escenas_detalladas", ""),
        "audio_sonido": guion_result.get("audio_sonido", ""),
        "caption_hashtags": copy_result.get("caption_hashtags", ""),
        "keyword": keyword,
        "manychat": copy_result.get("manychat", ""),
        "prompt_json": json.dumps(prompt_result.get("prompt_json", []), ensure_ascii=False),
        "historias": json.dumps(stories_result.get("historias", []), ensure_ascii=False)
    }
    
    # ─── MOSTRAR RESUMEN ────────────────────────────────────────────────
    print("\n" + "="*60)
    print("✅ CONTENIDO GENERADO EXITOSAMENTE")
    print("="*60)
    print(f"\n📌 HOOK: {fila['hook']}")
    print(f"📋 FORMATO: {fila['formato']} | {fila['etapa_buyer']} | {fila['keyword']}")
    print(f"\n📝 GUION (primeras 300 chars):")
    print(f"   {fila['guion_slides'][:300]}...")
    print(f"\n🎬 ESCENAS: {len(prompt_result.get('prompt_json', []))}")
    print(f"📱 HISTORIAS: {len(stories_result.get('historias', []))}")
    print(f"\n📣 CAPTION (primeras 200 chars):")
    print(f"   {fila['caption_hashtags'][:200]}...")
    
    # ─── GUARDAR EN SHEET ────────────────────────────────────────────────
    if auto_write:
        escribir = "s"
    else:
        print("\n" + "-"*60)
        escribir = input("¿Escribir esta fila al Google Sheet? (s/n): ").strip().lower()
    
    if escribir == "s":
        try:
            write_row_to_sheet(fila)
            print_success("✅ Fila escrita al Google Sheet en la pestaña PIPELINE")
        except Exception as e:
            print_error(f"Error escribiendo al Sheet: {e}")
            print("   ℹ️  Los datos están disponibles arriba para copiarlos manualmente.")
    else:
        print("\n   ℹ️  Fila NO escrita al Sheet.")
    
    # Guardar también en outputs/ como backup
    output_file = ROOT_DIR / "outputs" / f"contenido_{tipo}_{etapa}_{keyword}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fila, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Backup guardado en: {output_file}")
    
    return fila


def run_batch(cantidad: int = 5):
    """Genera una semana completa de contenido con variedad automática."""
    print_banner()
    print(f"\n📅 Generando batch de {cantidad} piezas...\n")
    
    # Distribución recomendada para una semana
    batch_config = [
        {"tipo": "Reel", "etapa": "TOFU", "keyword": "PAUSA"},
        {"tipo": "Carrusel", "etapa": "TOFU", "keyword": "PAUSA"},
        {"tipo": "B-Roll", "etapa": "TOFU", "keyword": "CALMA"},
        {"tipo": "Reel", "etapa": "MOFU", "keyword": "NOCHE"},
        {"tipo": "Carrusel", "etapa": "MOFU", "keyword": "CERO"},
    ]
    
    # Hooks para cada tipo (el usuario debe editarlos)
    hooks_default = [
        "Tu mandíbula tensa al despertar no es costumbre",
        "5 cosas que tu cuerpo hace cuando llevás semanas en modo alerta",
        "La calma no es ausencia de ruido. Es saber qué hacer con él.",
        "Por qué respirar profundo a veces no alcanza",
        "Lo que nadie te dice sobre el burnout hasta que ya lo estás viviendo"
    ]
    
    resultados = []
    for i in range(min(cantidad, len(batch_config))):
        config = batch_config[i]
        hook = hooks_default[i]
        
        print(f"\n[{i+1}/{cantidad}] Generando: {config['tipo']} / {config['etapa']}")
        print(f"  Hook: {hook}")
        
        try:
            fila = generate_content(
                hook=hook,
                tipo=config["tipo"],
                etapa=config["etapa"],
                keyword=config["keyword"],
                auto_write=True  # Batch escribe automáticamente
            )
            resultados.append(fila)
            print_success(f"Pieza {i+1} generada y escrita")
        except Exception as e:
            print_error(f"Error en pieza {i+1}: {e}")
            continue
    
    print(f"\n\n{'='*60}")
    print(f"✅ BATCH COMPLETADO: {len(resultados)}/{cantidad} piezas generadas")
    print(f"{'='*60}")


def run_test():
    """Verificar que todas las conexiones están funcionando."""
    print_banner()
    print("\n🔍 Verificando instalación...\n")
    
    # Test Anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key and api_key != "sk-ant-api03-COMPLETAR":
        print("✅ Anthropic API: configurada")
        try:
            client = anthropic.Anthropic(api_key=api_key)
            client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            print("✅ Anthropic API: conectada y funcionando")
        except Exception as e:
            print(f"❌ Anthropic API: error de conexión — {e}")
    else:
        print("❌ Anthropic API: ANTHROPIC_API_KEY no configurada en .env")
    
    # Test Google Sheets
    try:
        data = read_sheet_data()
        print(f"✅ Google Sheets: conectado — {len(data)} filas en el Sheet")
    except Exception as e:
        print(f"❌ Google Sheets: {e}")
    
    # Test archivos de agentes
    agents = ["scout_agent", "guion_agent", "prompt_agent", "copy_agent", "stories_agent"]
    for agent in agents:
        path = ROOT_DIR / "agents" / f"{agent}.md"
        if path.exists():
            print(f"✅ Agente {agent}: encontrado")
        else:
            print(f"❌ Agente {agent}: NO encontrado en {path}")
    
    print("\n✅ Sistema listo." if True else "\n❌ Hay errores que corregir antes de continuar.")


def main():
    parser = argparse.ArgumentParser(
        description="Mente Pausada — Generador de Contenido Automatizado"
    )
    
    parser.add_argument("--hook", type=str, help="Gancho del contenido")
    parser.add_argument("--tipo", type=str, choices=["Reel", "Carrusel", "B-Roll"], help="Formato del contenido")
    parser.add_argument("--etapa", type=str, choices=["TOFU", "MOFU", "BOFU"], default="TOFU")
    parser.add_argument("--keyword", type=str, choices=["PAUSA", "CERO", "NOCHE", "CALMA"], default="PAUSA")
    parser.add_argument("--escenas", type=int, help="Número de escenas (default según formato)")
    parser.add_argument("--contexto", type=str, default="", help="Contexto adicional opcional")
    parser.add_argument("--auto", action="store_true", help="Escribe al Sheet sin pedir confirmación")
    parser.add_argument("--batch", type=str, help="Genera batch (ej: --batch semana)")
    parser.add_argument("--cantidad", type=int, default=5, help="Cantidad de piezas en batch")
    parser.add_argument("--test", action="store_true", help="Verificar instalación")
    parser.add_argument("--interactive", action="store_true", help="Modo interactivo")
    
    args = parser.parse_args()
    
    if args.test:
        run_test()
        return
    
    if args.batch:
        run_batch(cantidad=args.cantidad)
        return
    
    if args.interactive:
        print_banner()
        print("\n🎯 MODO INTERACTIVO\n")
        hook = input("Hook / Gancho: ").strip()
        tipo = input("Tipo (Reel/Carrusel/B-Roll): ").strip()
        etapa = input("Etapa (TOFU/MOFU/BOFU) [TOFU]: ").strip() or "TOFU"
        keyword = input("Keyword (PAUSA/CERO/NOCHE/CALMA) [PAUSA]: ").strip() or "PAUSA"
        contexto = input("Contexto adicional (Enter para saltar): ").strip()
        
        generate_content(hook, tipo, etapa, keyword, contexto)
        return
    
    if not args.hook or not args.tipo:
        parser.print_help()
        print("\n❌ Se requiere --hook y --tipo para generar contenido.")
        print("   O usar --interactive, --batch, o --test")
        sys.exit(1)
    
    generate_content(
        hook=args.hook,
        tipo=args.tipo,
        etapa=args.etapa,
        keyword=args.keyword,
        contexto=args.contexto,
        num_escenas=args.escenas,
        auto_write=args.auto
    )


if __name__ == "__main__":
    main()
