# utils.py
import threading
import requests
import os
import logging

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"
BREVO_API_KEY = os.getenv("BREVO_API_KEY")

SENDER_EMAIL = "subhajeetkar449@gmail.com"  # MUST be verified in Brevo
SENDER_NAME = "Dharma AI"


def _send_email(subject, message, to_email):
    if not BREVO_API_KEY:
        logging.error("BREVO_API_KEY not set")
        return

    payload = {
        "sender": {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": message,
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    try:
        response = requests.post(
            BREVO_API_URL,
            json=payload,
            headers=headers,
            timeout=10
        )

        if response.status_code not in (200, 201, 202):
            logging.error(
                f"Brevo error {response.status_code}: {response.text}"
            )

    except Exception as e:
        logging.exception("Brevo email sending failed", exc_info=e)


def send_email_async(subject, message, from_email, recipient_list):
    if not recipient_list:
        return

    threading.Thread(
        target=_send_email,
        args=(subject, message, recipient_list[0]),
        daemon=True
    ).start()
