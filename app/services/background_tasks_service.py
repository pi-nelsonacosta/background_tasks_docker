import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL_ADDRESS = "nelsongacosta@gmail.com"
EMAIL_PASSWORD = "bodr wyvq xwik nqkv"

def write_log(message: str):
    # Simulamos escribir un log o realizar una tarea que lleva tiempo
    time.sleep(5)
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

def send_email(background_tasks):
    def send():
        try:
            msg = MIMEMultipart()
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = "nelsongacosta@gmail.com"
            msg['Subject'] = "Prueba de envío de correo"

            body = "Este es un correo enviado automáticamente después de 10 segundos."
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            text = msg.as_string()
            server.sendmail(EMAIL_ADDRESS, "nelsongacosta@gmail.com", text)
            server.quit()
            background_tasks.add_task(write_log, "Correo enviado exitosamente")
        except Exception as e:
            background_tasks.add_task(write_log, f"Error al enviar el correo: {e}")

    # Ejecutar la función de envío de correo después de 10 segundos
    time.sleep(10)
    send()