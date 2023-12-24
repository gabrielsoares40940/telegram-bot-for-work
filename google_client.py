from __future__ import print_function

import base64
import os.path
import re

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "13aEmBuLQdjJ567sdKLAlZcDDUAvbZ_n1fovDRTOpk9U"
SAMPLE_RANGE_NAME = "Class Data!A2:E"

class GmailClient:
    def __init__(self) -> None:
        self.authenticate()
        self.service = self.get_service()

    def authenticate(self):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if not hasattr(self, 'creds'):
            self.creds = None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

    def get_service(self):
        return build('sheets', 'v4', credentials=self.creds)

    def start_sheets(self, _value, _service, _payment_mehtod):
        try:
            service = build("sheets", "v4", credentials=self.creds)

            # Call the Sheets API
            sheet = service.spreadsheets()
            # result = (
            #     sheet.values()
            #     .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
            #     .execute()
            # )
            result = (
                sheet.values()
                .append(
                    spreadsheetId=SAMPLE_SPREADSHEET_ID,
                    range=SAMPLE_RANGE_NAME,
                    valueInputOption='USER_ENTERED',
                    body={'values': [[datetime.now().strftime('%d/%m/%Y %H:%M'), _service, _value, _payment_mehtod]]}
                ).execute()
            )
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

            print("Name, Major:")
            for row in values:
                # Print columns A and E, which correspond to indices 0 and 4.
                print(f"{row[0]}, {row[4]}")
        except HttpError as err:
            print(err)

    def get_emails_by_label_id(self, label_id: str):
        return self.service.users().messages().list(userId='me', q=f'label:{label_id}').execute()

    def get_email_by_id(self, id: str):
        return self.service.users().messages().get(userId='me', id=id).execute()

    def get_attachment_by_id(self, attachment_id: str, message_id: str):
        return self.service.users().messages().attachments().get(userId='me', messageId=message_id, id=attachment_id).execute()

    def write_file(self, data, filename):
        file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

        with open(filename, 'wb') as f:
            f.write(file_data)

    def get_billet_date(self, phrase: str) -> str:
        return re.findall(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', phrase)[0]