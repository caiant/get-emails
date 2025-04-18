import imaplib
import email
from datetime import datetime, timedelta
import os

def fetch_recent_emails():
    # Connect to IMAP server
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("GMAIL_ADDRESS"), os.getenv("GMAIL_APP_PASSWORD"))
    mail.select("inbox")

    # Calculate date 24 hours ago
    since_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

    # Search for emails since yesterday
    status, messages = mail.search(None, f'(SINCE "{since_date}")')
    email_ids = messages[0].split()

    for e_id in email_ids:
        _, msg_data = mail.fetch(e_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)

        print(f"\nSubject: {msg['subject']}")
        print(f"From: {msg['from']}")
        print(f"Date: {msg['date']}")

        # Get email body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    print(f"Body: {part.get_payload(decode=True).decode()[:200]}...")
                    break
        else:
            print(f"Body: {msg.get_payload(decode=True).decode()[:200]}...")

    mail.close()
    mail.logout()

if __name__ == "__main__":
    fetch_recent_emails()
