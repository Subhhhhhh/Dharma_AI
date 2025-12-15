import threading
import requests
import os

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


def _send_email(subject, message, to_email):
    api_key = os.getenv("BREVO_API_KEY")

    payload = {
        "sender": {
            "name": "Dharma AI",
            "email": "subhajeetkar449@gmail.com"  # verified sender
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": message,
    }

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json",
    }

    requests.post(BREVO_API_URL, json=payload, headers=headers, timeout=10)


def send_email_async(subject, message, from_email, recipient_list):
    threading.Thread(
        target=_send_email,
        args=(subject, message, recipient_list[0]),
        daemon=True
    ).start()
