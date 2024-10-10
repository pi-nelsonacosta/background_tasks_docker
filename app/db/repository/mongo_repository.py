import motor.motor_asyncio
from bson import ObjectId
from app.db.models.mongo_model import MongoModel

MONGO_URI = "mongodb://mongodb:27017"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.clean_architecture_db

async def get_mongo_record(record_id: str):
    if not ObjectId.is_valid(record_id):
        raise ValueError(f"'{record_id}' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string")
    
    record = await db["mongo_collection"].find_one({"_id": ObjectId(record_id)})

    if record:
        # Convertir el `_id` de ObjectId a string para que sea serializable
        record["id"] = str(record["_id"])
        del record["_id"]
    
    return record

async def create_mongo_record(data: MongoModel):
    # Insertar el documento en la base de datos
    result = await db["mongo_collection"].insert_one(data.dict(by_alias=True, exclude={"id"}))
    # Obtener el id insertado y devolverlo como string
    inserted_id = str(result.inserted_id)
    
    # Devolver el registro con el id asignado
    return {"id": inserted_id, **data.dict(exclude={"id"})}

async def update_mongo_record(record_id: str, data: dict):
    try:
        await db["mongo_collection"].update_one({"_id": ObjectId(record_id)}, {"$set": data})
        return await get_mongo_record(record_id)
    except Exception as e:
        raise ValueError(f"Invalid ObjectId: {e}")

async def delete_mongo_record(record_id: str):
    try:
        result = await db["mongo_collection"].delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count
    except Exception as e:
        raise ValueError(f"Invalid ObjectId: {e}")