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


port = 587
smtp_server = "smtp.gmail.com"
sender_email = "jhonpython61@gmail.com"
password = "recm ylge acie zhye"


def sendEmail(receiver_email, newSubject, newContent):
    message = EmailMessage()
    message.set_content(newContent)

    message["Subject"] = newSubject
    message["From"] = sender_email
    message["To"] = receiver_email

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    return


def sendMenu(receiver_email, menuAdapter):
    textContent = "This is an automated message, please do not reply to this email"
    mailSubject = "Menu requested"

    message = EmailMessage()
    message.set_content(textContent)

    message["Subject"] = mailSubject
    message["From"] = sender_email
    message["To"] = receiver_email

    menuFile = menuAdapter.generateContentFile()
    menuFileType = menuAdapter.getFileExtension()
    menuFileName = "menu." + menuFileType

    message.add_attachment(
        menuFile, maintype="application", subtype=menuFileType, filename=menuFileName
    )

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
    except smtplib.SMTPResponseException as error:
        print(f"Error: {error.smtp_error}")
        return error.smtp_code

    return smtplib.SMTPResponseException.smtp_code


if __name__ == "__main__":
    sendEmail("cascante.aldo@gmail.com", "Test", "This is a notification")
