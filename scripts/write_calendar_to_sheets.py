#!/usr/bin/env python3
"""
Calendario de Contenido 30 Días — Mayo 2026
Escribe el calendario completo a las hojas de Google Sheets de:
  - Mente Pausada  → tab 'Ideas Crudas'
  - Polt Mobilier  → tab 'Ideas Crudas'

Uso:
    python scripts/write_calendar_to_sheets.py

Requisitos:
    pip install gspread google-auth

Configuración:
    1. Colocar google-credentials.json en backend/credentials/
    2. Compartir ambas hojas con el email del service account (con rol Editor)
    3. Verificar que los tabs se llamen exactamente 'Ideas Crudas' y 'claude'
"""

import sys
import json
from pathlib import Path

# Fix: cryptography del sistema Debian está rota en Python 3.11.
# Insertamos la versión funcional instalada en /tmp/cryptography_new.
_CRYPTO_FIX = Path("/tmp/cryptography_new")
if _CRYPTO_FIX.exists() and str(_CRYPTO_FIX) not in sys.path:
    sys.path.insert(0, str(_CRYPTO_FIX))

try:
    import gspread
    from google.oauth2.service_account import Credentials
except ImportError:
    print("❌ Falta instalar dependencias:")
    print("   pip install gspread google-auth")
    print("   pip install cryptography --ignore-installed --target /tmp/cryptography_new")
    sys.exit(1)

# ─── RUTAS Y IDs ─────────────────────────────────────────────────────────────

ROOT = Path(__file__).parent.parent

CREDENTIALS_PATH = ROOT / "backend" / "credentials" / "google-credentials.json"

MENTE_PAUSADA_SHEET_ID = "1R-3TH3fsOJdcKObpE1PVrX8IPPw8Oca84TvamXBma1I"
POLT_SHEET_ID          = "1aYmSXVRyJamR9p5FWb2ADu6o2GbTcZ0k9bYZBN166Go"

TAB_IDEAS   = "Ideas Crudas"
TAB_CLAUDE  = "claude"          # para leer qué ya está hecho (evitar repetición)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ─── MAPEO DE COLUMNAS ───────────────────────────────────────────────────────
# Asocia fragmentos de nombre de header (lowercase) → clave del dict de contenido
COLUMN_MAP = {
    "falta":    "falta",
    "formato":  "formato",
    "gancho":   "gancho",
    "hook":     "gancho",
    "etapa":    "etapa_buyer",
    "buyer":    "etapa_buyer",
    "estado":   "estado",
    "guion":    "guion",
    "guión":    "guion",
    "escena":   "escenas",
    "audio":    "audio",
    "música":   "audio",
    "musica":   "audio",
    "caption":  "caption",
    "keyword":  "keyword",
    "manychat": "manychat",
    "prompt":   "prompts_json",
    "json":     "prompts_json",
    "histor":   "historias",
}

# ─── CONEXIÓN ────────────────────────────────────────────────────────────────

def get_client():
    if not CREDENTIALS_PATH.exists():
        print(f"\n❌ Credenciales no encontradas en:\n   {CREDENTIALS_PATH}")
        print("\n📋 Pasos para configurarlas:")
        print("   1. Creá una Service Account en console.cloud.google.com")
        print("   2. Descargá el JSON y ponelo en backend/credentials/google-credentials.json")
        print("   3. Compartí AMBAS hojas con el email del service account (rol: Editor)")
        print("   4. Volvé a correr este script\n")
        sys.exit(1)

    creds  = Credentials.from_service_account_file(str(CREDENTIALS_PATH), scopes=SCOPES)
    client = gspread.authorize(creds)
    return client


def get_done_hooks(client, sheet_id, tab_name=TAB_CLAUDE):
    """Lee el tab 'claude' y devuelve set de ganchos ya producidos (para evitar repetición)."""
    try:
        sheet     = client.open_by_key(sheet_id)
        worksheet = sheet.worksheet(tab_name)
        records   = worksheet.get_all_records()
        hooks = set()
        for r in records:
            for key in r:
                if "gancho" in key.lower() or "hook" in key.lower():
                    val = str(r[key]).strip().lower()
                    if val:
                        hooks.add(val)
        return hooks
    except Exception:
        return set()   # Si no existe el tab, continuar sin filtrar


def write_to_sheet(client, sheet_id, brand_name, rows):
    """
    Escribe una lista de dicts al tab 'Ideas Crudas' de la hoja indicada.
    Mapea automáticamente los keys del dict a las columnas según el header.
    """
    print(f"\n📊 Conectando a hoja de {brand_name}...")

    try:
        sheet = client.open_by_key(sheet_id)
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Hoja no encontrada: {sheet_id}")
        print(f"   → Verificá que el service account tiene acceso")
        return False

    # Intentar abrir el tab con variaciones de nombre
    worksheet = None
    for tab_variant in [TAB_IDEAS, "ideas crudas", "IDEAS CRUDAS", "Ideas crudas"]:
        try:
            worksheet = sheet.worksheet(tab_variant)
            print(f"   ✅ Tab encontrado: '{tab_variant}'")
            break
        except gspread.exceptions.WorksheetNotFound:
            continue

    if worksheet is None:
        print(f"❌ No se encontró el tab '{TAB_IDEAS}'")
        print(f"   → Tabs disponibles: {[ws.title for ws in sheet.worksheets()]}")
        return False

    # Leer headers
    headers = worksheet.row_values(1)
    if not headers:
        print("❌ El tab no tiene headers en la fila 1")
        return False

    print(f"   📋 Columnas detectadas ({len(headers)}): {headers}")

    # Encontrar próxima fila vacía
    all_values = worksheet.get_all_values()
    next_row   = len(all_values) + 1
    print(f"   📍 Escribiendo desde fila {next_row} ({len(rows)} posts)")

    # Construir matriz de valores según headers
    matrix = []
    for post in rows:
        row_values = []
        for header in headers:
            h = header.lower().strip()
            value = ""
            for fragment, key in COLUMN_MAP.items():
                if fragment in h:
                    value = post.get(key, "")
                    break
            # prompts_json: si es dict/list, convertir a string JSON
            if isinstance(value, (dict, list)):
                value = json.dumps(value, ensure_ascii=False, indent=2)
            row_values.append(str(value) if value else "")
        matrix.append(row_values)

    # Escribir en batch
    start_cell = f"A{next_row}"
    worksheet.update(start_cell, matrix, value_input_option="RAW")

    # Aplicar wrap text a las filas escritas
    try:
        sheet_meta  = worksheet._spreadsheet.fetch_sheet_metadata()
        sheet_id_num = None
        for s in sheet_meta["sheets"]:
            if s["properties"]["title"] == worksheet.title:
                sheet_id_num = s["properties"]["sheetId"]
                break
        if sheet_id_num is not None:
            requests = [{
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id_num,
                        "startRowIndex": next_row - 1,
                        "endRowIndex": next_row - 1 + len(rows),
                    },
                    "cell": {"userEnteredFormat": {
                        "wrapStrategy": "WRAP",
                        "verticalAlignment": "TOP"
                    }},
                    "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
                }
            }]
            sheet.batch_update({"requests": requests})
    except Exception:
        pass  # El formato es opcional, no bloquear

    print(f"   ✅ {len(rows)} posts escritos en '{worksheet.title}'")
    return True


# ─── MAIN ────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  CALENDARIO MAYO 2026 → GOOGLE SHEETS")
    print("=" * 60)

    # Importar contenido
    sys.path.insert(0, str(ROOT / "scripts"))
    from content.mente_pausada_mayo    import POSTS as MP_POSTS
    from content.polt_mobilier_mayo    import POSTS as POLT_POSTS

    client = get_client()
    print("✅ Conectado a Google Sheets")

    # ── Mente Pausada ──
    done_mp = get_done_hooks(client, MENTE_PAUSADA_SHEET_ID)
    if done_mp:
        print(f"\n   ℹ️  {len(done_mp)} ganchos ya producidos en tab 'claude' (se omitirán duplicados)")
    mp_nuevos = [p for p in MP_POSTS if p["gancho"].lower() not in done_mp]
    write_to_sheet(client, MENTE_PAUSADA_SHEET_ID, "Mente Pausada", mp_nuevos)

    # ── Polt Mobilier ──
    done_polt = get_done_hooks(client, POLT_SHEET_ID)
    if done_polt:
        print(f"\n   ℹ️  {len(done_polt)} ganchos ya producidos en tab 'claude' (se omitirán duplicados)")
    polt_nuevos = [p for p in POLT_POSTS if p["gancho"].lower() not in done_polt]
    write_to_sheet(client, POLT_SHEET_ID, "Polt Mobilier", polt_nuevos)

    print("\n" + "=" * 60)
    print(f"  LISTO — {len(mp_nuevos)} posts MP + {len(polt_nuevos)} posts Polt escritos")
    print("=" * 60)


if __name__ == "__main__":
    main()
