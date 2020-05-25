"""
Generic helpers for fetching data from Google Spreadsheets.
"""
import google.auth
import gspread


def gsheets_api_connect():
    creds, project_id = google.auth.default(scopes=gspread.auth.DEFAULT_SCOPES)

    return gspread.authorize(creds)


def get_sheet_rows(spreadsheet_name, sheet_name):
    conn = gsheets_api_connect()
    spreadsheet = conn.open(spreadsheet_name)
    sheet = spreadsheet.worksheet(sheet_name)
    rows = sheet.get_all_values()
    return rows
