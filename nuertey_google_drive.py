import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Project name: nuertey-google-drive-python
# Project ID: helical-sled-278320
#
# Name: Google Drive API
# Service name: drive.googleapis.com
# Overview: The Google Drive API allows clients to access resources from Google Drive.
# Activation status: Enabled
#
# Application name: nuertey-google-drive
# OAuth 2.0 client ID: Web client 1
# Authorized JavaScript origins: http://localhost:8080
# Authorized redirect URIs: http://localhost:8080

# Via github comments:
#gauth = GoogleAuth()
#scope = ['https://www.googleapis.com/auth/drive']
#gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
#drive = GoogleDrive(gauth)

#my_file = drive.CreateFile({'id': 'FILE_ID'}) 

# PyDrive Way:
gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Creates local webserver and auto handles authentication.
drive = GoogleDrive(gauth)

file1 = drive.CreateFile({'title': 'Hello.txt'})  # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello World!') # Set content of the file from given string.
file1.Upload()

# Auto-iterate through all files that matches this query
file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
for file2 in file_list:
  print('title: %s, id: %s' % (file2['title'], file2['id']))

print()

# Paginate file lists by specifying number of max results
for file_list in drive.ListFile({'maxResults': 100}):
    print('Received {} files from Files.list()'.format(len(file_list))) # <= 100
    for file3 in file_list:
        print('title: {}, id: {}'.format(file3['title'], file3['id']))
