import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 587))

def send_email(to: str, subject: str, body: str) -> str:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to

    text_body = body.replace("\\n", "\n")
    html_body = "<html><body><p>" + text_body.replace("\n", "<br>") + "</p></body></html>"

    msg.attach(MIMEText(text_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to], msg.as_string())
    return f"Email envoyé à {to} avec sujet '{subject}'"
