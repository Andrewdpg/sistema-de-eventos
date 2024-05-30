from email.message import EmailMessage
from dotenv import load_dotenv
import ssl
import smtplib
import os

load_dotenv()

email_sender = os.getenv('EMAIL_SENDER')
email_password = os.getenv('EMAIL_PASSWORD')

subject = 'University Verification Code'
em = EmailMessage()

context = ssl.create_default_context()

def send_email(email, verification_code):
    email_receiver = email
    body = """
    Hola, tu codigo de verificación es: %s
    """ % (verification_code)

    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    
    em.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())