import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.db.repository.mongo_repository import create_mongo_record
from sqlalchemy.orm import Session
from app.db.repository.mysql_repository import create_mysql_record
import asyncio

EMAIL_ADDRESS = "nelsongacosta@gmail.com"
EMAIL_PASSWORD = "bodr wyvq xwik nqkv"

async def write_log(db: Session, message: str):
    # 1. Insertar en MySQL
    log_record = create_mysql_record(db, message)
    print(f"Log guardado en MySQL con ID: {log_record.id}")
    
    # 2. Insertar en MongoDB
    mongo_data = {"message": message}
    mongo_id = await create_mongo_record(mongo_data)
    print(f"Log guardado en MongoDB con ID: {mongo_id}")
    
    # 3. Escribir en archivo de texto
    with open("log.txt", "a") as log_file:
        log_file.write(f"MySQL ID: {log_record.id}, MongoDB ID: {mongo_id}, Mensaje: {message}\n")

def send_email(delay_seconds: int, message: str):
    # Esperar el tiempo especificado antes de enviar el correo
    time.sleep(delay_seconds)
    
    try:
        # Preparar el correo
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = "nelsongacosta@gmail.com"
        msg['Subject'] = "Prueba de envío de correo"

        body = f"Este es un correo enviado automáticamente después de {delay_seconds} segundos. El mensaje enviado fue: {message}"
        msg.attach(MIMEText(body, 'plain'))

        # Enviar el correo
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_ADDRESS, "nelsongacosta@gmail.com", text)
        server.quit()

        print("Correo enviado exitosamente")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")