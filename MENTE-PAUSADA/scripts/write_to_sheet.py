"""
write_to_sheet.py — Escribe una fila completa al Google Sheet CONTENIDO_MENTEPAUSADA
"""

import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / ".env")


def get_sheets_service():
    """Inicializa y retorna el servicio de Google Sheets API."""
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    
    credentials_path = ROOT_DIR / os.getenv("GOOGLE_CREDENTIALS_PATH", "config/credentials.json")
    creds = Credentials.from_service_account_file(
        str(credentials_path),
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    service = build("sheets", "v4", credentials=creds)
    return service


def get_next_empty_row(service, sheet_id: str, sheet_name: str) -> int:
    """Encuentra la próxima fila vacía en el Sheet."""
    range_name = f"{sheet_name}!A:A"
    result = service.spreadsheets().values().get(
        spreadsheetId=sheet_id,
        range=range_name
    ).execute()
    
    values = result.get("values", [])
    return len(values) + 1  # +1 porque Sheets es 1-indexed


def write_row_to_sheet(fila: dict) -> bool:
    """
    Escribe una fila de contenido al Google Sheet.
    
    La fila debe tener estos campos (en orden de columnas del Sheet):
    numero, formato, hook, etapa_buyer, estado, guion_slides, escenas_detalladas,
    audio_sonido, caption_hashtags, keyword, manychat, prompt_json, historias
    """
    service = get_sheets_service()
    sheet_id = os.getenv("GOOGLE_SHEET_ID")
    sheet_name = os.getenv("SHEET_NAME", "PIPELINE")
    
    if not sheet_id:
        raise ValueError("GOOGLE_SHEET_ID no configurado en .env")
    
    # Preparar los valores en el orden correcto de columnas
    row_values = [
        fila.get("numero", ""),
        fila.get("formato", ""),
        fila.get("hook", ""),
        fila.get("etapa_buyer", ""),
        fila.get("estado", "Idea"),
        fila.get("guion_slides", ""),
        fila.get("escenas_detalladas", ""),
        fila.get("audio_sonido", ""),
        fila.get("caption_hashtags", ""),
        fila.get("keyword", ""),
        fila.get("manychat", ""),
        fila.get("prompt_json", ""),
        fila.get("historias", "")
    ]
    
    # Convertir todo a string (el Sheet no acepta otros tipos)
    row_values = [str(v) if v is not None else "" for v in row_values]
    
    # Encontrar la próxima fila vacía
    next_row = get_next_empty_row(service, sheet_id, sheet_name)
    range_name = f"{sheet_name}!A{next_row}"
    
    # Escribir la fila
    body = {"values": [row_values]}
    
    result = service.spreadsheets().values().update(
        spreadsheetId=sheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    
    updated_cells = result.get("updatedCells", 0)
    print(f"   📊 Fila {next_row} escrita — {updated_cells} celdas actualizadas")
    
    # Aplicar formato de wrap text a la fila (para que el contenido largo se vea bien)
    try:
        apply_wrap_format(service, sheet_id, sheet_name, next_row)
    except Exception as e:
        print(f"   ⚠️  No se pudo aplicar formato: {e} (no es crítico)")
    
    return True


def apply_wrap_format(service, sheet_id: str, sheet_name: str, row_number: int):
    """Aplica wrap text a la fila recién escrita."""
    # Obtener el ID de la hoja por nombre
    sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
    sheet_id_num = None
    for sheet in sheet_metadata.get("sheets", []):
        if sheet["properties"]["title"] == sheet_name:
            sheet_id_num = sheet["properties"]["sheetId"]
            break
    
    if sheet_id_num is None:
        return
    
    requests = [{
        "repeatCell": {
            "range": {
                "sheetId": sheet_id_num,
                "startRowIndex": row_number - 1,
                "endRowIndex": row_number,
                "startColumnIndex": 0,
                "endColumnIndex": 13
            },
            "cell": {
                "userEnteredFormat": {
                    "wrapStrategy": "WRAP",
                    "verticalAlignment": "TOP"
                }
            },
            "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"
        }
    }]
    
    service.spreadsheets().batchUpdate(
        spreadsheetId=sheet_id,
        body={"requests": requests}
    ).execute()


if __name__ == "__main__":
    # Test con una fila de prueba
    test_row = {
        "numero": 999,
        "formato": "TEST",
        "hook": "TEST — esta fila se puede borrar",
        "etapa_buyer": "TOFU",
        "estado": "Test",
        "guion_slides": "Guion de prueba",
        "escenas_detalladas": "Escenas de prueba",
        "audio_sonido": "Audio de prueba",
        "caption_hashtags": "Caption de prueba #test",
        "keyword": "PAUSA",
        "manychat": "Mensaje de prueba",
        "prompt_json": "[]",
        "historias": "[]"
    }
    
    try:
        write_row_to_sheet(test_row)
        print("✅ Escritura de prueba exitosa")
    except Exception as e:
        print(f"❌ Error: {e}")
