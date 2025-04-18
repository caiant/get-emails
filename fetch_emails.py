import yagmail
from datetime import datetime, timedelta
import os

def fetch_recent_emails():
    # Authenticate (using environment variables)
    yag = yagmail.SMTP(
        user=os.getenv("GMAIL_ADDRESS"),
        password=os.getenv("GMAIL_APP_PASSWORD"),  # Use App Password if 2FA enabled
        host="smtp.gmail.com"
    )

    # Calculate 24 hours ago
    since_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")

    # Fetch emails
    emails = yag.inbox(
        label="INBOX",
        since=since_date,
        limit=20  # Adjust as needed
    )

    # Process results
    for email in emails:
        print(f"\nSubject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Date: {email['date']}")
        print(f"Body Preview: {email['body'][:200]}...")  # First 200 chars

if __name__ == "__main__":
    fetch_recent_emails()
