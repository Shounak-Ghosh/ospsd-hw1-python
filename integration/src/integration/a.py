# from google_auth_oauthlib.flow import InstalledAppFlow

# SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes=SCOPES)
# creds = flow.run_local_server(port=8000)

# print("Access Token:", creds.token)
# print("Refresh Token:", creds.refresh_token)

# authorize_gmail.py
import os
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=8000)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("Access and refresh tokens saved to token.json")

if __name__ == '__main__':
    main()
