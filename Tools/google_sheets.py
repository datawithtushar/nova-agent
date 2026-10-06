from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain.tools import tool


# Paths & Credentials for Google Sheets API
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1NArWF9RZDiXNeXshv_3BNfi-r0fNlujOkTuq_Ni71Rk"
BASE_DIR = Path(__file__).resolve().parent.parent
CREDENTIALS_FILE = BASE_DIR / "credentials.json"
TOKEN_FILE = BASE_DIR / "token.json"


# Getting the Google Sheets service & Authentication
def get_service():
    credentials = None

    if TOKEN_FILE.exists():
        credentials = Credentials.from_authorized_user_file(
            TOKEN_FILE,
            SCOPES
        )

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "w") as file:
            file.write(credentials.to_json())

    return build("sheets","v4",credentials=credentials)


# 1) Reading data from the subscription tracker
@tool
def read_subscriptions():
    """Read all subscription records from the subscription tracker."""

    service = get_service()
    result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range="Sheet1!A1:Z100").execute()

    return result.get("values", [])


# 2) Write Tool for writing data to the subscription tracker multiple values at once
@tool
def update_subscriptions(updates: dict):
    """Update multiple fields for one or more subscriptions."""

    service = get_service()
    rows = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,range="Sheet1!A1:Z100").execute().get("values", [])

    headers = rows[0]
    subscription_column = headers.index("Subscription")

    updated = []

    for subscription_name, fields in updates.items():

        for row_number, row in enumerate(rows[1:], start=2):

            if row[subscription_column].lower() == subscription_name.lower():

                for column_name, new_value in fields.items():

                    if column_name not in headers:
                        continue

                    target_column = headers.index(column_name)
                    column_letter = chr(65 + target_column)

                    service.spreadsheets().values().update(
                        spreadsheetId=SPREADSHEET_ID,
                        range=f"Sheet1!{column_letter}{row_number}",
                        valueInputOption="USER_ENTERED",
                        body={
                            "values": [[new_value]]
                        }
                    ).execute()

                updated.append(subscription_name)
                break

    return f"Updated subscriptions: {', '.join(updated)}"


# 3) Adding new multiple subscription to the tracker
@tool
def add_subscriptions(subscriptions: list[dict]):
    """Add one or more new subscriptions to the tracker.
    Each subscription should include:
    Subscription, Start Date, Licenses, Price Annually (GBP), Status"""

    service = get_service()

    new_rows = []

    for subscription in subscriptions:
        new_row = [
            "",
            subscription["Subscription"],
            subscription["Start Date"],
            subscription["Licenses"],
            "",
            "",
            "",
            subscription["Price Annually (GBP)"],
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            subscription["Status"]
        ]

        new_rows.append(new_row)

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Sheet1!A:R",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={
            "values": new_rows
        }
    ).execute()

    return f"{len(new_rows)} subscription(s) added successfully."