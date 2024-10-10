from sqlalchemy.orm import Session
from app.db.models.mysql_model import MySQLModel

def get_mysql_record(db: Session, record_id: int):
    return db.query(MySQLModel).filter(MySQLModel.id == record_id).first()

def create_mysql_record(db: Session, name: str, description: str = None):
    db_record = MySQLModel(name=name, description=description)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def update_mysql_record(db: Session, record_id: int, name: str = None, description: str = None):
    db_record = db.query(MySQLModel).filter(MySQLModel.id == record_id).first()
    if db_record:
        if name:
            db_record.name = name
        if description:
            db_record.description = description
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_mysql_record(db: Session, record_id: int):
    db_record = db.query(MySQLModel).filter(MySQLModel.id == record_id).first()
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record
