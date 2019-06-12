from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive']


l_sr = []
l_id = []
l_name = []

def store(name, ids, cnt):
    global l_sr
    l_sr = l_sr + [int(cnt)]
    global l_id
    l_id = l_id + [ids]
    global l_name
    l_name = l_name + [name]


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, description)").execute()
    items = results.get('files', [])

    print("Torrents in Google Drive Before File Upload: \n\n")

    cnt = 0
    if not items:
        print('No files found. \n')
    else:
        for item in items:
            name = item['name']
            ids = item['id']
            dex = item['description']
            print(u'Serial Number = {0} ||File_Id = {1} || Name = {2} || Description = {3}'.format(cnt, ids, name, dex))
            store(name, ids, cnt)
            cnt  = cnt + 1


    global l_sr
    global l_name
    global l_id
    arr = []
    for i in l_sr:
        arr = arr + [(i, l_name[i], l_id[i])]
    
    #sr = int(input('sr no'))
    filename = input("Enter FileName: \n")
    filepath = input("Enter FilePath including FileName: \n")
    file_description = input("Enter a description for the contents of this .torrent!\n")
    mimetype = 'application/zip' # searching for .torrent mimetype but zip works fine too!
    file_metadata = {'name': filename, 'description': file_description}
    media = MediaFileUpload(filepath, mimetype=mimetype)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name, description)").execute()
    items = results.get('files', [])

    cnt = 0
    if not items:
        print('No files found. \n')
    else:
        print('The Files after recent upload: \n')
        for item in items:
            name = item['name']
            ids = item['id']
            dex = item['description']
            print(u'Serial Number = {0} ||File_Id = {1} || Name = {2} || Description = {3}'.format(cnt, ids, name, dex))
            store(name, ids, cnt)
            cnt  = cnt + 1


if __name__ == '__main__':
    main()
