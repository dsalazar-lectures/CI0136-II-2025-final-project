import os
import smtplib
from email.message import EmailMessage

smtp_server = os.getenv("SMTP_SERVER", "localhost")
smtp_port = int(os.getenv("SMTP_PORT", 1025))
smtp_user = os.getenv("SMTP_USER", "")
smtp_password = os.getenv("SMTP_PASSWORD", "")


def send_email(sender, recipient, subject, contents):
    message = EmailMessage()
    message.set_content(contents)

    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as s:
        s.send_message(message)


if __name__ == "__main__":
    send_email(
        "sender@example.com",
        "recipient@example.com",
        "Test Subject",
        "This is a test email.",
    )
