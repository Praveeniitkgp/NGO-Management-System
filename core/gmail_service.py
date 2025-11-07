# Gmail API service for sending emails
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def get_gmail_service():
    creds = None
    token_path = os.path.join(os.path.dirname(__file__), 'token.pickle')
    credentials_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
    
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing token: {e}")
                creds = None
        
        if not creds:
            client_id = os.getenv('GMAIL_CLIENT_ID', '')
            client_secret = os.getenv('GMAIL_CLIENT_SECRET', '')
            refresh_token = os.getenv('GMAIL_REFRESH_TOKEN', '')
            
            if client_id and client_secret and refresh_token:
                from google.oauth2.credentials import Credentials
                creds = Credentials(
                    token=None,
                    refresh_token=refresh_token,
                    token_uri='https://oauth2.googleapis.com/token',
                    client_id=client_id,
                    client_secret=client_secret,
                    scopes=SCOPES
                )
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token from env vars: {e}")
                    creds = None
            
            if not creds and os.path.exists(credentials_path):
                try:
                    if os.path.exists(token_path):
                        pass
                    else:
                        print("token.pickle not found. Please run generate_refresh_token.py first.")
                        return None
                except Exception as e:
                    print(f"Error loading credentials.json: {e}")
                    return None
            
            if not creds:
                print("Gmail OAuth2 credentials not configured. Please set GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, and GMAIL_REFRESH_TOKEN in .env")
                return None
        
        if creds:
            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)
    
    try:
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(f"Error building Gmail service: {e}")
        return None


def send_email_gmail_api(to_email, subject, message_text, from_email=None):
    try:
        service = get_gmail_service()
        if not service:
            return False
        
        message = MIMEText(message_text)
        message['to'] = to_email
        message['subject'] = subject
        if from_email:
            message['from'] = from_email
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        send_message = {'raw': raw_message}
        result = service.users().messages().send(
            userId='me',
            body=send_message
        ).execute()
        
        print(f"Email sent successfully. Message ID: {result.get('id')}")
        return True
        
    except Exception as e:
        print(f"Error sending email via Gmail API: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

