from os import getenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(title: str, body: str, receiver: list[str]):
  smtp_host = getenv("AWS_SES_SMTP_HOST", "email-smtp.eu-west-2.amazonaws.com")
  smtp_port = int(getenv("AWS_SES_SMTP_PORT", "587"))
  smtp_user = getenv("AWS_SERVER_PUBLIC_KEY", "")
  smtp_pass = getenv("AWS_SERVER_SECRET_KEY", "")
  sender = getenv("EMAIL_SENDER", "Scholub <scholub@schale.misile.xyz>")

  for i in receiver:
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = i
    msg["Subject"] = title
    msg.attach(MIMEText(body, "html", "utf-8"))

    with smtplib.SMTP(smtp_host, smtp_port) as server:
      _ = server.starttls()
      _ = server.login(smtp_user, smtp_pass)
      _ = server.sendmail(sender, i, msg.as_string())

