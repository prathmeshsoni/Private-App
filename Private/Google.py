import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


def Create_Service(api_name, api_version, prefix=''):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version

    cred = None
    working_dir = os.getcwd()
    print(working_dir)

    print(os.listdir(working_dir))
    token_file = working_dir + '/Private/' + 'token_drive_v3.pickle'
    print(token_file)
    try:
        with open(token_file, 'rb') as token:
            cred = pickle.load(token)
    except Exception as e:
        print('ees', e)

    if not cred or not cred.valid:
        print("pickle.load(token)")
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            pass
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        return None
