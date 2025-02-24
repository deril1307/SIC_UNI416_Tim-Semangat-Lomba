import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["sensor_db"]
collection = db["sensor_data"]
result = collection.delete_many({})
print(f"{result.deleted_count} dokumen telah dihapus.")
