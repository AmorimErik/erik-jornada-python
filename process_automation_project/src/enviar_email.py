import os
from pathlib import Path
import smtplib
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

ROOT_PATH = Path(__file__).parent.parent

load_dotenv()


def enviar_email(data_indicador, loja, caminho, destinatario, corpo_email):
    msg = MIMEMultipart()
    msg["Subject"] = (
        f"OnePage {data_indicador.day}/{data_indicador.month} - Loja {loja}"
    )
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = destinatario
    msg.HTMLBody = corpo_email

    msg.attach(MIMEText(corpo_email, "html"))

    # anexar arquivos
    with open(caminho, "rb") as arquivo:
        msg.attach(MIMEApplication(arquivo.read(), Name=caminho))

    servidor = smtplib.SMTP("smtp.gmail.com", 587)
    servidor.starttls()
    servidor.login(msg["From"], os.getenv("LOGGIN"))
    servidor.send_message(msg)
    servidor.quit()
    print("Email enviado")
