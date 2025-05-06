"""Authorize Gmail API and save credentials.

This script uses the Google OAuth 2.0 flow to authorize access to the Gmail API
and saves the credentials to a `token.json` file for future use.
"""

from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def main() -> None:
    """Run the OAuth 2.0 flow to authorize Gmail API access and save credentials."""
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=8000)
    with Path("token.json").open("w") as token:
        token.write(creds.to_json())

if __name__ == "__main__":
    main()
