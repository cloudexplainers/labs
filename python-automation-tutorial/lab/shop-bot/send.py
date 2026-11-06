import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

shop = Path.home() / "shop"
HOST = os.environ.get("SMTP_HOST", "localhost")
PORT = int(os.environ.get("SMTP_PORT", "1025"))


def run():
    msg = EmailMessage()
    msg["From"] = "shop-bot@anas-tea.test"
    msg["To"] = "ben@anas-tea.test"
    msg["Subject"] = "This week's tea report"
    msg.set_content("Hi Ben, the sales report and the invoices are attached.")
    for name in ["report.xlsx", "invoices-all.pdf"]:
        data = (shop / name).read_bytes()
        msg.add_attachment(data, maintype="application",
                           subtype="octet-stream", filename=name)

    with smtplib.SMTP(HOST, PORT) as smtp:
        if os.environ.get("SMTP_USER"):  # a real server wants a login
            smtp.starttls()
            smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(msg)
    print(f"Sent \"{msg['Subject']}\" to {msg['To']}")


if __name__ == "__main__":
    run()
