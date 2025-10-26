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

def send_file(receiver_email):
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = "jhonpython61@gmail.com"
    password = "recm ylge acie zhye"
    contents = "Test"

    message = EmailMessage()
    message.set_content(contents)

    message["Subject"] = "test.py"
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


if __name__ == "__main__":
    send_file("cascante.aldo@gmail.com")

