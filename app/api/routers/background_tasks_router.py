from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.background_tasks_service import write_log, send_email
from app.db.repository.mysql_repository import (get_mysql_record, create_mysql_record, update_mysql_record, delete_mysql_record)
from app.db.repository.mongo_repository import (get_mongo_record, create_mongo_record, update_mongo_record, delete_mongo_record)
from app.db.session import SessionLocal
from app.db.models.mongo_model import MongoModel

router = APIRouter()

# Dependencia para la sesión de la base de datos

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/send-log/")
async def send_log(message: str, background_tasks: BackgroundTasks):
    # Agregar la tarea al fondo para que se ejecute después de responder
    background_tasks.add_task(write_log, message)
    # Agregar tarea para enviar correo después de 10 segundos
    background_tasks.add_task(send_email, background_tasks)
    return {"message": "El log se enviará en segundo plano y el correo se enviará después de 10 segundos"}

@router.post("/mysql-record/")
async def create_mysql(name: str, description: str, db: Session = Depends(get_db)):
    return create_mysql_record(db, name, description)

@router.get("/mysql-record/{record_id}")
async def read_mysql(record_id: int, db: Session = Depends(get_db)):
    record = get_mysql_record(db, record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.put("/mysql-record/{record_id}")
async def update_mysql(record_id: int, name: str = None, description: str = None, db: Session = Depends(get_db)):
    return update_mysql_record(db, record_id, name, description)

@router.delete("/mysql-record/{record_id}")
async def delete_mysql(record_id: int, db: Session = Depends(get_db)):
    return delete_mysql_record(db, record_id)

@router.post("/mongo-record/")
async def create_mongo(data: MongoModel):
    return await create_mongo_record(data)

@router.get("/mongo-record/{record_id}")
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

