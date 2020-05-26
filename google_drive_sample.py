import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# =====================================================================
# Setup the following Google Cloud Project and Google Drive parameters 
# as per the links below. Save your parameters in the ??? designated 
# below :
# 
# https://pythonhosted.org/PyDrive/quickstart.html#authentication
# console.cloud.google.com
# drive.google.com
# =====================================================================
# Project name: ???
# Project ID: ???
#
# Name: Google Drive API
# Service name: drive.googleapis.com
# Overview: The Google Drive API allows clients to access resources from Google Drive.
# Activation status: Enabled
#
# Application name: ???
# OAuth 2.0 client ID: ???
# Authorized JavaScript origins: http://localhost:8080
# Authorized redirect URIs: http://localhost:8080

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
