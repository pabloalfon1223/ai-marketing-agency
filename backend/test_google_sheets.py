#!/usr/bin/env python3
"""
Test script for Google Sheets integration

Usage:
    python test_google_sheets.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import get_settings
from app.services.google_auth import GoogleAuthService
from app.database import AsyncSessionLocal
from app.services.sheets_sync import SheetsSyncService


async def test_google_auth():
    """Test Google authentication"""
    print("\n" + "=" * 60)
    print("Testing Google Sheets Authentication")
    print("=" * 60)

    settings = get_settings()

    print(f"\n📋 Configuration:")
    print(f"  Sheet ID: {settings.google_sheets_id or '❌ NOT SET'}")
    print(f"  Credentials Path: {settings.google_credentials_path}")
    print(f"  File Exists: {'✅' if os.path.exists(settings.google_credentials_path) else '❌'}")

    # Test client initialization
    print(f"\n🔑 Initializing Google Sheets client...")
    client = GoogleAuthService.get_gspread_client()

    if client:
        print("✅ Google Sheets client initialized successfully!")
        return True
    else:
        print("❌ Failed to initialize Google Sheets client")
        print("\nPossible causes:")
        print("  1. Credentials file not found")
        print("  2. Invalid JSON in credentials")
        print("  3. gspread/google-auth packages not installed")
        print("  4. GOOGLE_CREDENTIALS_JSON not set")
        return False


async def test_sheet_access():
    """Test accessing a Google Sheet"""
    print("\n" + "=" * 60)
    print("Testing Sheet Access")
    print("=" * 60)

    settings = get_settings()

    if not settings.google_sheets_id:
        print("\n⚠️  GOOGLE_SHEETS_ID not set in .env")
        print("   Cannot test sheet access without a sheet ID")
        return False

    print(f"\n📊 Attempting to access sheet: {settings.google_sheets_id}")

    sheet = GoogleAuthService.open_sheet(settings.google_sheets_id)
    if sheet:
        print(f"✅ Sheet opened successfully!")
        print(f"   Title: {sheet.title}")

        # List worksheets
        worksheets = sheet.worksheets()
        print(f"\n📑 Found {len(worksheets)} worksheet(s):")
        for ws in worksheets:
            print(f"   - {ws.title} ({ws.cell_count} cells)")

        return True
    else:
        print("❌ Failed to access sheet")
        print("\nPossible causes:")
        print("  1. Sheet ID is incorrect")
        print("  2. Service account doesn't have access to sheet")
        print("  3. Sheet has been deleted")
        return False


async def test_sync():
    """Test sync operation"""
    print("\n" + "=" * 60)
    print("Testing Synchronization")
    print("=" * 60)

    settings = get_settings()

    if not settings.google_sheets_id:
        print("\n⚠️  GOOGLE_SHEETS_ID not set, skipping sync test")
        return False

    print(f"\n🔄 Testing sync with sheet: {settings.google_sheets_id}")

    try:
        async with AsyncSessionLocal() as db:
            sync_service = SheetsSyncService(settings.google_sheets_id, db)

            # Test POTENCIALES sync
            print("\n📥 Syncing POTENCIALES...")
            result = await sync_service.sync_potenciales()
            print(f"   Created: {result.get('created', 0)}")
            print(f"   Updated: {result.get('updated', 0)}")
            print(f"   Converted: {result.get('converted', 0)}")
            if result.get("error"):
                print(f"   ❌ Error: {result['error']}")
            else:
                print("   ✅ POTENCIALES sync successful")

            # Test PRODUCCION sync
            print("\n📥 Syncing PRODUCCION...")
            result = await sync_service.sync_produccion()
            print(f"   Created: {result.get('created', 0)}")
            print(f"   Updated: {result.get('updated', 0)}")
            if result.get("error"):
                print(f"   ❌ Error: {result['error']}")
            else:
                print("   ✅ PRODUCCION sync successful")

        return True

    except Exception as e:
        print(f"\n❌ Sync test failed: {str(e)}")
        import traceback

        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "🧪 GOOGLE SHEETS INTEGRATION TEST SUITE" + "\n")

    # Test 1: Authentication
    auth_ok = await test_google_auth()

    if not auth_ok:
        print(
            "\n\n⛔ Cannot proceed without working authentication"
        )
        return

    # Test 2: Sheet Access
    sheet_ok = await test_sheet_access()

    if not sheet_ok:
        print("\n⚠️  Cannot test sync without sheet access")
        return

    # Test 3: Sync
    await test_sync()

    # Summary
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Review the output above for any errors")
    print("  2. If all passed, the backend is ready for syncing")
    print("  3. Monitor the logs: cat logs/app.log")
    print("  4. Check dashboard at: http://localhost:5173/dashboards")


if __name__ == "__main__":
    asyncio.run(main())
