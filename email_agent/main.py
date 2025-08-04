import os
import re
import requests
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
EMAIL = os.getenv("EMAIL_USERNAME")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("EMAIL_SMTP", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 587))


def mistral_chat_completion(prompt: str):
    url = "https://api.mistral.ai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
    "model": "mistral-small-latest",
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.5,
    }
    resp = requests.post(url, headers=headers, json=data)
    if not resp.ok:
        print("Status:", resp.status_code)
        print("Response:", resp.text)
        resp.raise_for_status()

    return resp.json()["choices"][0]["message"]["content"]


def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, [to], msg.as_string())
    return f"Email sent to {to} with subject '{subject}'"


def parse_and_execute(command):
    # Try extracting email info via Mistral
    extraction_prompt = f"""
You are an assistant that extracts structured email data from user commands.
Given this instruction: "{command}", extract:
- the recipient's email address
- a smart subject line
- a polite and full email body that fits the request

Respond in this JSON format:
{{
  "to": "...",
  "subject": "...",
  "body": "..."
}}
"""
    try:
        reply = mistral_chat_completion(extraction_prompt)
        # extract JSON fields manually (Mistral doesn't do true JSON)
        to = re.search(r'"to"\s*:\s*"([^"]+)"', reply).group(1)
        subject = re.search(r'"subject"\s*:\s*"([^"]+)"', reply).group(1)
        body = re.search(r'"body"\s*:\s*"([^"]+)"', reply, re.DOTALL).group(1)
        return send_email(to.strip(), subject.strip(), body.strip())
    except Exception as e:
        return f"Failed to extract email details: {e}"


if __name__ == "__main__":
    print("AI Email Agent ready. Type 'exit' to quit.")
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ("exit", "quit"):
            break
        output = parse_and_execute(user_input)
        print(output)
