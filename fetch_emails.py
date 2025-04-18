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

        # Print bold & underlined subject
        print("\n\033[1;4m" + msg['subject'] + "\033[0m")  # Bold underline formatting
        
        # Get and print body text
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        
        print("\n" + body.strip() + "\n")
        print("-" * 50)  # Separator line

    mail.close()
    mail.logout()

if __name__ == "__main__":
    fetch_recent_emails()
    mail.logout()

if __name__ == "__main__":
    fetch_recent_emails()
