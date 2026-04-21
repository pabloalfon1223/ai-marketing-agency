"""
Google Sheets Authentication and Client Management

Handles OAuth2 credentials and gspread client initialization
for Google Sheets API access.
"""

import json
import os
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)


class GoogleAuthService:
    """Service for managing Google Sheets authentication"""

    _client = None
    _sheets_client = None

    @classmethod
    def get_gspread_client(cls):
        """
        Get or initialize gspread client for Google Sheets access

        Returns:
            gspread.Client or None if credentials not available
        """
        if cls._client is not None:
            return cls._client

        try:
            import gspread
            from google.oauth2.service_account import Credentials

            settings = get_settings()

            # Try to load credentials from file or JSON string
            credentials_data = None

            if settings.google_credentials_json:
                # Parse inline JSON credentials
                credentials_data = json.loads(settings.google_credentials_json)
                logger.info("Loaded Google credentials from GOOGLE_CREDENTIALS_JSON")

            elif os.path.exists(settings.google_credentials_path):
                # Load from file
                with open(settings.google_credentials_path, "r") as f:
                    credentials_data = json.load(f)
                logger.info(
                    f"Loaded Google credentials from {settings.google_credentials_path}"
                )
            else:
                logger.warning(
                    f"Google credentials not found at {settings.google_credentials_path}"
                )
                return None

            # Create credentials object
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive",
            ]

            credentials = Credentials.from_service_account_info(
                credentials_data, scopes=scopes
            )

            # Authorize gspread client
            cls._client = gspread.authorize(credentials)
            logger.info("Google Sheets client initialized successfully")

            return cls._client

        except ImportError:
            logger.error(
                "gspread not installed. Run: pip install gspread google-auth-oauthlib google-auth-httplib2"
            )
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in Google credentials: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error initializing Google Sheets client: {str(e)}")
            return None

    @classmethod
    def open_sheet(cls, sheet_id: str):
        """
        Open a Google Sheet by ID

        Args:
            sheet_id: Google Sheet ID

        Returns:
            gspread.Spreadsheet or None if error
        """
        try:
            client = cls.get_gspread_client()
            if not client:
                logger.error("Google client not available")
                return None

            sheet = client.open_by_key(sheet_id)
            logger.info(f"Opened sheet: {sheet.title}")
            return sheet

        except Exception as e:
            logger.error(f"Error opening sheet {sheet_id}: {str(e)}")
            return None

    @classmethod
    def get_worksheet(cls, sheet_id: str, worksheet_name: str):
        """
        Get a specific worksheet by name

        Args:
            sheet_id: Google Sheet ID
            worksheet_name: Name of the worksheet tab

        Returns:
            gspread.Worksheet or None if error
        """
        try:
            sheet = cls.open_sheet(sheet_id)
            if not sheet:
                return None

            worksheet = sheet.worksheet(worksheet_name)
            logger.info(f"Retrieved worksheet: {worksheet_name}")
            return worksheet

        except Exception as e:
            logger.error(
                f"Error getting worksheet {worksheet_name}: {str(e)}"
            )
            return None

    @classmethod
    def reset_client(cls):
        """Reset the gspread client (useful for testing)"""
        cls._client = None
        logger.info("Google Sheets client reset")
