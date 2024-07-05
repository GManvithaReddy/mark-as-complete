from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.search import GmailSearch
from langchain_community.tools.gmail.utils import build_resource_service, get_gmail_credentials
import os
import base64
import csv
from extra.state import State

class Nodes:
    def check_email(self, state):
        print("# Checking for new emails")
        
        # Define email criteria
        email_address = 'manvithareddy1309@gmail.com'

        # Initialize Gmail API
        api_resource = build_resource_service(credentials=get_gmail_credentials(
            token_file='token.json',
            scopes=["https://mail.google.com/"],
            client_secrets_file="credentials.json",
        ))
        
        # Perform Gmail search for emails from specific email address
        search_query = f'in:inbox from:{email_address}'
        search = GmailSearch(api_resource=api_resource)
        emails = search(search_query)

        # Get the latest email if available and not already checked
        latest_email = None
        checked_emails = state['checked_emails_ids'] if state['checked_emails_ids'] else []

        for email in emails:
            if email['id'] not in checked_emails:
                latest_email = {
                    "id": email['id'],
                    "threadId": email["threadId"],
                    "subject": email["subject"],
                    "body": email["body"],
                    "sender": email["sender"]
                }
                break  # Stop after finding the first eligible email

        # Update state with the latest email found
        new_emails = [] if latest_email is None else [latest_email]
        checked_emails.append(latest_email['id'])

        return {
            **state,
            "emails": new_emails,
            "checked_emails_ids": checked_emails
        }

    def extract_attachments(self, state, save_directory='attachments'):
        api_resource = build_resource_service(credentials=get_gmail_credentials(
            token_file='token.json',
            scopes=["https://mail.google.com/"],
            client_secrets_file="credentials.json",
        ))

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for email in state['emails']:
            message = api_resource.users().messages().get(userId='me', id=email['id']).execute()
            for part in message['payload'].get('parts', []):
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        attachment_id = part['body']['attachmentId']
                        attachment = api_resource.users().messages().attachments().get(
                            userId='me', messageId=email['id'], id=attachment_id
                        ).execute()
                        data = attachment['data']

                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))

                    if part['filename'].endswith('.csv'):
                        # Save the CSV file locally
                        file_path = os.path.join(save_directory, part['filename'])
                        with open(file_path, 'wb') as f:
                            f.write(file_data)
                        print(f"Downloaded CSV file: {file_path}")

        return {
            **state,
            "file_name": file_path,
        }

    def extract_data(self, state: State):
        timestamps = []
        load_numbers = []

        with open(state["file_name"], 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                timestamps.append(row.get('TIMESTAMP'))
                load_numbers.append(row.get('LOAD_NUMBER'))

        return {
            **state,
            "timestamps": timestamps,
            "load_numbers": load_numbers,
            "tracking_ids": [],
            "stop_ids": [],
            "iso_strings": []
        }
