from langchain.tools import tool
import os
import smtplib
from email.message import EmailMessage

# A tool to draft an email
@tool
def draft_email(recipients: list[str],subject: str,body: str):
    """Prepare an email draft for one or more recipients."""

    return {
        "recipients": recipients,
        "subject": subject,
        "body": body,
        "status": "Draft"
    }


# A tool to send an email
@tool
def send_email(recipients: list[str],subject: str,body: str):
    """Send an approved email to one or more recipients."""

    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_ADDRESS")
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_SERVER"),int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_ADDRESS"),os.getenv("EMAIL_PASSWORD"))
        server.send_message(message)

    return "Email sent successfully."