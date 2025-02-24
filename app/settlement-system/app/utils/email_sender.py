import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import smtplib

def send_email_advisement(to_email, pdf_file):
    """
    Sends an email advisement with the PDF attachment.
    """
    msg = MIMEMultipart()
    msg['From'] = 'your_email@example.com'
    msg['To'] = to_email
    msg['Subject'] = 'Settlement Advisement'

    with open(pdf_file, "rb") as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {pdf_file}")
        msg.attach(part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('your_email@example.com', 'your_email_password')
        smtp.send_message(msg)
