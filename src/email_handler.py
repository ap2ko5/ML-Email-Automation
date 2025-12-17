"""
Email Handler Module

Handles email retrieval, parsing, and sending operations.
"""

import os
import pickle
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_core.retry import Retry
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class EmailHandler:
    """Handle email operations with Gmail API"""

    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

    def __init__(self, credentials_path=None):
        """Initialize email handler"""
        self.credentials_path = credentials_path or 'config/credentials.json'
        self.service = self._authenticate()

    def _authenticate(self):
        """Authenticate with Gmail API"""
        creds = None
        
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def fetch_emails(self, label='INBOX', unread_only=True, max_results=10):
        """Fetch emails from Gmail
        
        Args:
            label: Gmail label to fetch from
            unread_only: Only fetch unread emails
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries
        """
        try:
            query = f'label:{label}'
            if unread_only:
                query += ' is:unread'

            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            emails = []

            for msg in messages:
                email_data = self._parse_email(msg['id'])
                if email_data:
                    emails.append(email_data)

            return emails

        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def _parse_email(self, msg_id):
        """Parse individual email message
        
        Args:
            msg_id: Gmail message ID
            
        Returns:
            Email dictionary
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=msg_id,
                format='full'
            ).execute()

            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
            
            body = self._get_email_body(message['payload'])

            return {
                'id': msg_id,
                'subject': subject,
                'from': sender,
                'body': body,
                'raw': message
            }

        except Exception as e:
            print(f'Error parsing email {msg_id}: {e}')
            return None

    def _get_email_body(self, payload):
        """Extract email body from payload
        
        Args:
            payload: Email payload
            
        Returns:
            Email body text
        """
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8')
        else:
            data = payload['body'].get('data', '')
            if data:
                return base64.urlsafe_b64decode(data).decode('utf-8')
        
        return ''

    def send_email(self, to, subject, body):
        """Send an email
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            
        Returns:
            Message ID if successful, None otherwise
        """
        try:
            message = MIMEText(body)
            message['to'] = to
            message['subject'] = subject
            
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            send_message = {'raw': raw_message}
            
            result = self.service.users().messages().send(
                userId='me',
                body=send_message
            ).execute()
            
            return result['id']

        except HttpError as error:
            print(f'Error sending email: {error}')
            return None

    def mark_as_read(self, msg_id):
        """Mark email as read
        
        Args:
            msg_id: Gmail message ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.service.users().messages().modify(
                userId='me',
                id=msg_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except HttpError as error:
            print(f'Error marking email as read: {error}')
            return False
