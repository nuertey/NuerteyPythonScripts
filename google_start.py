import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Stock API Way:
scopes = ['https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scopes)
http_auth = credentials.authorize(Http())
drive = build('drive','v3',http=http_auth)

response = drive.files().list().execute()
