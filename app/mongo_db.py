import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

mongo_db = client["telecom_ai_db"]

logs_collection = mongo_db["network_logs"]

