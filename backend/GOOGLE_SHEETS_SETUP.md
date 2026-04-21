# Google Sheets Integration Setup

This document explains how to set up Google Sheets authentication for the Polt Mobilier system.

## Prerequisites

1. A Google Cloud Platform (GCP) project
2. Google Sheets API enabled
3. A Service Account with credentials

## Step-by-Step Setup

### 1. Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click "Select a Project" → "New Project"
3. Name it "Polt Mobilier" (or your preference)
4. Click "Create"

### 2. Enable Google Sheets API

1. In the Cloud Console, search for "Google Sheets API"
2. Click on it and press "Enable"

### 3. Create a Service Account

1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Fill in:
   - Service Account Name: `polt-mobilier-sheets`
   - Click "Create and Continue"
4. Grant roles:
   - Role: "Editor" (or "Spreadsheet Editor" if available)
   - Click "Continue"
5. Click "Done"

### 4. Create and Download Credentials

1. In Service Accounts list, click on the account you just created
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Click "Create"
6. A JSON file will download automatically

### 5. Set Up Credentials in Your Project

#### Option A: Using Credentials File (Recommended for development)

1. Create a `credentials` folder in the backend directory:
   ```bash
   mkdir backend/credentials
   ```

2. Move the downloaded JSON file to this folder:
   ```bash
   mv ~/Downloads/your-service-account-key.json backend/credentials/google-credentials.json
   ```

3. Update your `.env` file:
   ```
   GOOGLE_CREDENTIALS_PATH=./credentials/google-credentials.json
   GOOGLE_SHEETS_ID=your-sheet-id-here
   ```

4. Add `credentials/` to `.gitignore`:
   ```bash
   echo "credentials/" >> backend/.gitignore
   ```

#### Option B: Using Environment Variable (Better for production)

1. Encode the JSON file as base64:
   ```bash
   base64 -i backend/credentials/google-credentials.json | tr -d '\n'
   ```

2. Or just copy the JSON content and set in `.env`:
   ```
   GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}
   ```

### 6. Get Your Google Sheet ID

1. Create a new Google Sheet (or use an existing one)
2. Open it in your browser
3. The URL will look like: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
4. Copy the `SHEET_ID_HERE` part
5. Add to your `.env`:
   ```
   GOOGLE_SHEETS_ID=SHEET_ID_HERE
   ```

### 7. Share the Sheet with the Service Account

1. Open your Google Sheet
2. Click "Share" (top right)
3. Copy the service account email from the JSON file (looks like: `polt-mobilier-sheets@project.iam.gserviceaccount.com`)
4. Paste it in the share dialog
5. Give it "Editor" access
6. Click "Share"

### 8. Create Sheet Tabs

Your Google Sheet should have two tabs:

#### Tab 1: POTENCIALES

Columns (in order):
- `NOMBRE` - Client name
- `MUEBLE` - Product type
- `FECHA_CONTACTO` - Contact date (ISO format: YYYY-MM-DD)
- `ESTADO` - Status (SIN_RESPUESTA, ESPERAMOS_RESPUESTA, COTIZACION_ENVIADA, QUOTE_ACCEPTED)
- `QUIEN_LO_TIENE` - Assigned salesperson
- `TELEFONO` - Contact phone
- `NOTA` - Additional notes
- `FECHA_SEGUIMIENTO` - Follow-up date
- `VALOR_ESTIMADO` - Estimated value (numeric)

#### Tab 2: PRODUCCION

Columns (in order):
- `ORDEN_ID` - Order ID (unique, e.g., ORD-001-2026)
- `CLIENTE` - Client name
- `MUEBLE` - Product type
- `ESTADO` - Status (ACCEPTED, IN_PRODUCTION, COMPLETED, DELIVERED)
- `FECHA_INICIO` - Start date (ISO format: YYYY-MM-DD)
- `FECHA_ENTREGA_EST` - Estimated delivery date
- `PRODUCTOR` - Producer name
- `COSTO_REAL` - Actual cost (numeric)
- `PRECIO_FINAL` - Final price (numeric)
- `NOTAS_PRODUCCION` - Production notes

### 9. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 10. Test the Connection

Run the backend and check the logs:

```bash
cd backend
uvicorn app.main:app --reload
```

Look for messages like:
```
INFO:     Loaded Google credentials from ./credentials/google-credentials.json
INFO:     Google Sheets client initialized successfully
INFO:     APScheduler started: Sheets sync scheduled for every 10 minutes
```

## Troubleshooting

### "Google credentials not found"
- Ensure the credentials file path is correct in `.env`
- Check that the file exists and is readable

### "Invalid JSON in Google credentials"
- Verify the JSON file is valid (paste it at [jsonlint.com](https://jsonlint.com))
- Make sure you didn't paste additional text

### "Permission denied" errors
- Ensure the service account email is shared with the Google Sheet with Editor access
- Double-check the sheet ID is correct

### "Could not access POTENCIALES sheet"
- Verify the sheet tab names are exactly "POTENCIALES" and "PRODUCCION" (case-sensitive)
- Check that the sheet exists in your Google Sheets document

### Sync not running
- Check backend logs for scheduler startup message
- Ensure `GOOGLE_SHEETS_ID` is set in `.env`
- Wait 10 minutes for the first sync, or check the logs for errors

## API Endpoints for Manual Sync

While automatic sync runs every 10 minutes, you can also manually trigger:

```bash
# Get sync status (check logs)
curl http://localhost:8000/api/v1/health

# Manual API endpoints (if added)
# POST /api/v1/admin/sync-potenciales
# POST /api/v1/admin/sync-produccion
```

## Security Notes

⚠️ **Important:**
- Never commit `credentials/google-credentials.json` to Git
- Keep the service account email private
- Rotate credentials regularly in GCP
- Use environment variables for production deployment
- Consider using Google Cloud Secret Manager for production

## Support

If you encounter issues:
1. Check the backend logs for error messages
2. Verify all configuration steps above
3. Test the connection with a simple Python script:

```python
from app.services.google_auth import GoogleAuthService

client = GoogleAuthService.get_gspread_client()
if client:
    print("✅ Google Sheets client initialized successfully")
else:
    print("❌ Failed to initialize Google Sheets client")
```
