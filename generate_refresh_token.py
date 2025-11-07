
#!/usr/bin/env python3
# Generate Gmail API refresh token
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    credentials_path = 'credentials.json'
    if not os.path.exists(credentials_path):
        print("Error: credentials.json not found!")
        print("\nSteps to get credentials.json:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a project or select existing one")
        print("3. Enable Gmail API")
        print("4. Go to APIs & Services → Credentials")
        print("5. Create OAuth 2.0 Client ID (Web application)")
        print("6. Download credentials and save as 'credentials.json'")
        return
    
    print("Starting OAuth flow...")
    print("A browser window will open. Please log in and authorize the application.\n")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        credentials_path, SCOPES)
    creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=True)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    
    print("\nOAuth flow completed successfully!")
    print(f"\nAdd these to your .env file:")
    print(f"GMAIL_CLIENT_ID={creds.client_id}")
    print(f"GMAIL_CLIENT_SECRET={creds.client_secret}")
    print(f"GMAIL_REFRESH_TOKEN={creds.refresh_token}")
    print("\nToken saved to token.pickle")

if __name__ == '__main__':
    main()

