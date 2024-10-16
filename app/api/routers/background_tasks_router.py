from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.background_tasks_service import send_repeated_email, write_log, send_email
from app.db.session import SessionLocal
from app.db.models.mongo_model import MongoModel
from app.db.repository.mysql_repository import delete_all_mysql_records, get_all_mysql_records
from app.db.repository.mongo_repository import get_all_mongo_records, delete_all_mongo_records

router = APIRouter()

# Dependencia para la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/send-mail/")
async def send_mail(message: str, background_tasks: BackgroundTasks, delay_seconds: int, db: Session = Depends(get_db)):
    # Programar la escritura del log como una tarea en segundo plano
    await write_log(db, message)
    # Agregar tarea para enviar correo después del tiempo especificado (manteniéndolo sincrónico)
    background_tasks.add_task(send_email, delay_seconds, message)
    return {"message": f"El log se enviará en segundo plano y el correo se enviará después de {delay_seconds} segundos"}

@router.post("/send-repeated-mails/")
async def send_repeated_mails(background_tasks: BackgroundTasks, delay_seconds: int, repetitions: int, db: Session = Depends(get_db)):
    # Agregar tarea para enviar correos repetidamente en segundo plano
    background_tasks.add_task(send_repeated_email, delay_seconds, repetitions, db)
    return {"message": f"El correo se enviará {repetitions} veces, con un retraso de {delay_seconds} segundos entre cada envío."}

@router.get("/mysql-records/")
async def read_all_mysql_records(db: Session = Depends(get_db)):
    records = get_all_mysql_records(db)
    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records

@router.get("/mongo-records/")
async def read_all_mongo_records():
    records = await get_all_mongo_records()
    if not records:
        raise HTTPException(status_code=404, detail="No records found")
    return records

@router.delete("/mysql-records")
async def delete_all_mysql(db: Session = Depends(get_db)):
    delete_all_mysql_records(db)
    return {"message": "All MySQL records deleted"}

@router.delete("/mongo-records")
async def delete_all_mongo():
    deleted_count = await delete_all_mongo_records()
    return {"message": f"All MongoDB records deleted: {deleted_count} records"}

""" @router.post("/mysql-record/")
async def create_mysql(description: str, 
                       db: Session = Depends(get_db)):
    return create_mysql_record(db, description) """

""" @router.get("/mysql-record/{record_id}")
async def read_mysql(record_id: int, db: Session = Depends(get_db)):
    record = get_mysql_record(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/mysql-record/{record_id}")
async def update_mysql(record_id: int, name: str = None, 
                       description: str = None, 
                       db: Session = Depends(get_db)):
    return update_mysql_record(db, record_id, name, description)

@router.delete("/mysql-record/{record_id}")
async def delete_mysql(record_id: int, db: Session = Depends(get_db)):
    return delete_mysql_record(db, record_id) """

""" @router.post("/mongo-record/")
async def create_mongo(data: MongoModel):
    return await create_mongo_record(data) """

""" @router.get("/mongo-record/{record_id}")
async def read_mongo(record_id: str):
    record = await get_mongo_record(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/mongo-record/{record_id}")
async def update_mongo(record_id: str, data: dict):
    return await update_mongo_record(record_id, data)

@router.delete("/mongo-record/{record_id}")
async def delete_mongo(record_id: str):
    return await delete_mongo_record(record_id)
 """
