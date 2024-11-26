import base64
from authentication import *

def get_emails_with_attachments(service, senders):
    query = 'has:attachment ' + ' OR '.join([f'from:{sender}' for sender in senders])
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    if not messages:
        print("No messages found.")
        return
    os.makedirs(save_directory, exist_ok=True)

    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        if 'payload' in msg and 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['filename']:
                    print(f"Email ID: {message['id']}")
                    print(f"Attachment: {part['filename']}")
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute()
                    data = attachment['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = os.path.join(save_directory, part['filename'])
                    with open(path, 'wb') as f:
                        f.write(file_data)
                    print(f"Attachment saved to {path}")

if __name__ == '__main__':
    service = authenticate_gmail()
    specific_emails = [
        "MAIL_ID",
        "MAIL_ID",
        "MAIL_ID"
        "MAIL_ID"
        "MAIL_ID"
    ]
    save_directory = r"C:\ipASSIGNMENTSv4"
    get_emails_with_attachments(service, specific_emails)
