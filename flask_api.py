from flask import Flask, request, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)

# Gunakan MONGO_URI dari .env
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["sensor_db"]
collection = db["sensor_data"]

@app.route("/", methods=["GET"])
def home():
    return "Flask API untuk ESP32 dan MongoDB Atlas Berjalan!"

@app.route("/sensor", methods=["POST"])
def receive_data():
    """Menerima data dari ESP32 dan menyimpannya ke MongoDB"""
    data = request.json
    # Validasi apakah data lengkap
    if not data or "temperature" not in data or "humidity" not in data or "motion" not in data:
        return jsonify({"error": "Data tidak lengkap"}), 400

    # Simpan ke MongoDB
    result = collection.insert_one(data)
    
    if result.inserted_id:
        return jsonify({"message": "Data berhasil disimpan ke MongoDB"}), 200
    else:
        return jsonify({"error": "Gagal menyimpan data"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
