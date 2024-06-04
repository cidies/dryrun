import smtplib
from email.mime.text import MIMEText
import json
import logging

def email(title, description):
    config_path = 'c:\\temp\\config.json'
    with open(config_path, 'r') as f:
        config = json.load(f)

    server = config.get('email_server')
    port = 25
    username = config.get('email_user')
    password = config.get('email_password')
    sender = config.get('email_from')
    receiver = config.get('email_to')
    subject = title
    body = description

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

    try:
        smtp_server = smtplib.SMTP(server, port)
        smtp_server.ehlo()
        smtp_server.starttls()
        smtp_server.login(username, password)
        smtp_server.sendmail(sender, receiver, msg.as_string())
        smtp_server.close()
        logging.info(f"[emailnote] Sent email notification with title: {title} and description: {description}")
    except Exception as e:
        logging.error(f"[emailnote] Failed to send email notification with title: {title} and description: {description}. Error: {e}")
