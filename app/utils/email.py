import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.conf import settings


def send_email(to_email: str, subject: str, text: str, html: str = None) -> bool:
    """Sends email from SMTP provided in settings. Returns True if sent"""
    sender_email = settings.SMTP_USERNAME
    password = settings.SMTP_PASSWORD
    smtp_port = settings.SMTP_PORT
    smtp_host = settings.SMTP_HOST

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = to_email

    text_body = MIMEText(text, 'plain')
    message.attach(text_body)
    if html:
        html_body = MIMEText(html, 'html')
        message.attach(html_body)

    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
        server.set_debuglevel(1)
        try:
            server.login(sender_email, password)
            server.sendmail(
                sender_email, to_email, message.as_string()
            )
        except smtplib.SMTPAuthenticationError as err:
            print(
                'SMTP Credentials appear to be incorrect. The server didn’t accept the username/password combination.\n', err
            )
            return False
        except smtplib.SMTPException as err:
            print('There was an unknown problem sending email', err)
            return False
    return True
