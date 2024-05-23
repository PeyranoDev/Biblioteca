from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import bcrypt
from dotenv import load_dotenv

load_dotenv()

class AdminManager:
    def __init__(self):
        uri = os.getenv("MONGO_URL2")
        database = os.getenv("DB_NAME")
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client[database]
        self.admins = self.db["admins"]

    def add_admin(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.admins.insert_one({"username": username, "password": hashed_password})
        return "Admin added successfully"
    
a = AdminManager()

print(a.add_admin("admin", "12345"))