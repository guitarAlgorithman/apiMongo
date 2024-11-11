# database.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["gt"]
questions_collection = db["preguntas"]

async def save_web_data_if_empty(web_data):
    existing_count = await questions_collection.count_documents({})
    if existing_count == 0:
        result = await questions_collection.insert_many(web_data)
        print(f"{len(result.inserted_ids)} documentos insertados en MongoDB")
    else:
        print("La colección ya contiene datos, no se insertaron nuevos documentos.")

async def save_feedback(question, chosen_answer):
    await questions_collection.update_one(
        {"question": question},
        {"$set": {"answer": chosen_answer}},
        upsert=True
    )
