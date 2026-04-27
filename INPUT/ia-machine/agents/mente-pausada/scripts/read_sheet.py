"""
read_sheet.py — Lee datos del Google Sheet CONTENIDO_MENTEPAUSADA
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")


def get_sheets_service():
    """Inicializa y retorna el servicio de Google Sheets API."""
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    
    credentials_path = ROOT_DIR / os.getenv("GOOGLE_CREDENTIALS_PATH", "config/credentials.json")
    
    if not credentials_path.exists():
        raise FileNotFoundError(
            f"Archivo de credenciales no encontrado en: {credentials_path}\n"
            "Seguí el PASO 5 del SETUP.md para configurar las credenciales de Google."
        )
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly"
    ]
    
    creds = Credentials.from_service_account_file(str(credentials_path), scopes=scopes)
    service = build("sheets", "v4", credentials=creds)
    return service


def read_sheet_data(max_rows: int = 50) -> list:
    """
    Lee las últimas N filas del Google Sheet.
    Retorna lista de dicts con los campos de cada fila.
    """
    service = get_sheets_service()
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("SHEET_NAME", "PIPELINE")
    
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID no configurado en .env")
    
    # Leer el rango completo
    range_name = f"{sheet_name}!A:M"  # Columnas A hasta M (13 columnas)
    
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()
    
    values = result.get("values", [])
    
    if not values:
        return []
    
    # La primera fila es el header
    headers = values[0] if values else []
    
    # Columnas que necesitamos para el Scout
    columnas_scout = {
        0: "numero",
        1: "formato",
        2: "hook",
        3: "etapa_buyer",
        4: "estado",
        6: "escenas_detalladas",
        8: "caption_hashtags",
        9: "keyword",
        11: "prompt_json"
    }
    
    rows = []
    data_rows = values[1:]  # Saltar header
    
    # Tomar las últimas max_rows filas
    recent_rows = data_rows[-max_rows:] if len(data_rows) > max_rows else data_rows
    
    for row in recent_rows:
        if not row or (len(row) > 0 and not any(row)):
            continue
        
        row_dict = {}
        for col_idx, field_name in columnas_scout.items():
            if col_idx < len(row):
                row_dict[field_name] = row[col_idx]
            else:
                row_dict[field_name] = ""
        
        rows.append(row_dict)
    
    return rows


def extract_visual_patterns(sheet_data: list) -> list:
    """
    Extrae patrones visuales del campo escenas_detalladas para
    detectar repetición. Retorna lista de strings con los patrones encontrados.
    """
    patrones = []
    
    for row in sheet_data:
        escenas = row.get("escenas_detalladas", "")
        prompt_json_str = row.get("prompt_json", "")
        
        # Buscar patrones comunes en el texto
        texto = (escenas + " " + prompt_json_str).lower()
        
        patrones_conocidos = [
            ("mujer frotándose sienes", "frot" in texto and "sien" in texto),
            ("manos con taza de café", "mano" in texto and "café" in texto),
            ("persona en cama", "cama" in texto),
            ("cerrando laptop", "laptop" in texto and "cerr" in texto),
            ("texto sobre fondo negro", "fondo negro" in texto and "text" in texto),
            ("persona mirando ventana", "ventana" in texto),
            ("caminando en la calle", "caminando" in texto and "calle" in texto),
            ("manos escribiendo", "escribiendo" in texto or "libreta" in texto),
        ]
        
        for patron_nombre, condicion in patrones_conocidos:
            if condicion:
                patrones.append(patron_nombre)
    
    return patrones


if __name__ == "__main__":
    # Test directo
    try:
        data = read_sheet_data()
        print(f"✅ Sheet leído: {len(data)} filas")
        if data:
            print(f"Última fila: {data[-1].get('hook', 'sin hook')}")
    except Exception as e:
        print(f"❌ Error: {e}")
