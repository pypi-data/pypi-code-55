import pickle
import os.path
import re
from datetime import datetime
from operator import itemgetter
from itertools import groupby, dropwhile

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

class Base:
    spreadsheet_id = None
    sheet_name = None
    creds = None
    service = None

    def __init__(self, spreadsheet_id, sheet_name):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name

    def get_service(self):
        if not self.service:
            self.service = build('sheets', 'v4', credentials=self.auth())
        return self.service
    
    def auth(self):
        if self.creds and self.creds.valid:
            return self.creds

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        return self.creds

class Reader(Base):
    _info = None
    _col_headers = None
    _row_headers = None
    _rows = None

    def read_range(self, range):
        # Call the Sheets API
        service = self.get_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=range).execute()
        values = result.get('values', [])

        return values

    def read_info_about(self, title):
        request = self.get_service().spreadsheets().get(spreadsheetId=self.spreadsheet_id)
        response = request.execute()

        # deal with sheets with only one sheet
        return next(filter(lambda s: title in s['properties']['title'], response['sheets']))

    def load_info(self):
        info = self.read_info_about(self.sheet_name)
        props = info['properties']
        grid_props = props['gridProperties']
        frozen_row_count = grid_props['frozenRowCount'] if 'frozenRowCount' in grid_props else 0
        frozen_col_count = grid_props['frozenColumnCount'] if 'frozenColumnCount' in grid_props else 0

        self._info = {
            'sheet_id': props['sheetId'],
            'title': props['title'],
            'start_row': frozen_row_count + 1,
            'start_col_idx': frozen_col_count,
            'start_col': chr(65 + frozen_col_count)
        }

    def load_col_headers(self):
        if self.start_row == 1:
            self._col_headers = []
        else:
            target_range = '%s!%s%s:%s%s' % (self.title, self.start_col, self.start_row - 1, self.start_col, self.start_col)
            self._col_headers = next(iter(self.read_range(target_range)), [])

    def __getattr__(self, attr):
        if attr in ['title', 'start_row', 'start_col', 'sheet_id', 'start_col_idx']:
            if self._info is None:
                self.load_info()
            return self._info[attr]
        if attr in ['col_headers']:
            if self._col_headers is None:
                self.load_col_headers()
            return self._col_headers
        if attr in ['rows']:
            if self._rows is None:
                rng = '%s!%s%s:%s' % (self.title, self.start_col, self.start_row, 'ZZ')
                self._rows = self.read_range(rng)
            return self._rows

class Writer(Reader):
    _updates = []
    _additions = []
    _removals = []

    def remove(self, row):
        raise NotImplemented()

    def update(self, row, idxs, value=lambda i:i):
        # Find runs of consecutive numbers using groupby.
        for k, g in groupby(enumerate(idxs), lambda ix: ix[0] - ix[1]):
            group_idxs = list(map(itemgetter(1), g))
            col_offset = group_idxs[0]

            self._updates.append({
                "updateCells": {
                    'fields': '*',
                    'range': {
                        'sheetId': self.sheet_id,
                        'startRowIndex': row - 1,
                        'endRowIndex': row,
                        'startColumnIndex': self.start_col_idx + col_offset,
                        'endColumnIndex': self.start_col_idx + col_offset + len(group_idxs)
                    },
                    "rows": {
                        'values': [self.gvalue(value(idx)) for idx in group_idxs]
                    }
                }
            })

        print("\tQueud update to row %s" % (row))

    def append(self, idxs, value=lambda i:i):
        self._additions.append({
            "appendCells": {
                'sheetId': self.sheet_id,
                'fields': 'userEnteredValue',
                "rows": {
                    'values': [self.gvalue(value(idx)) for idx in idxs]
                }
            }
        })

        print("\tQueued row to be appended")

    def gvalue(self, value):
        if isinstance(value, (int, float, complex)):
            return {
                'userEnteredValue': {
                    'numberValue': value
                }
            }

        if isinstance(value, (str)):
            return {
                'userEnteredValue': {
                    'stringValue': value
                }
            }

        return {} # telling gsheet api to leave the column untouched

    def batch_update(self, requests):
        return self.get_service().spreadsheets().batchUpdate(
            spreadsheetId=self.spreadsheet_id,
            body={ 
                'requests': requests
            }
        ).execute()

    def commit(self):
        if len(self._updates + self._additions):
            _res = self.batch_update(self._updates + self._additions)
            # since we applies change immidiately need to force refreshing rows before further processing
            self._rows = None

        if self._updates != []:
            rows_updated = set([req["updateCells"]["range"]['startRowIndex'] + 1 for req in self._updates])
            print('\tUpdated rows %s' % ', '.join(map(str, rows_updated)))
            self._updates = []
        
        if self._additions != []:
            print('\tAdded %s new rows' % len(self._additions))
            self._additions = []
