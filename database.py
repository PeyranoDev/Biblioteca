import os
import logging
from pymongo import MongoClient
from dotenv import load_dotenv
import bcrypt

load_dotenv()

logging.basicConfig(filename='biblioteca.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

class Database:
    def __init__(self):
        mongo_url = os.getenv("MONGO_URL2")
        database = os.getenv("DB_NAME")
        self.client = MongoClient(mongo_url)
        self.db = self.client[database]
        self.books_collection = self.db["books"]
        self.books_collection.create_index("title") 
        self.admins_collection = self.db["admins"]
        
    

    def find_one_admin(self, query):
        return self.admins_collection.find_one(query)

    def insert_one_book(self, book):
        return self.books_collection.insert_one(book)

    def update_one_book(self, query, update):
        return self.books_collection.update_one(query, update)

    def delete_one_book(self, query):
        return self.books_collection.delete_one(query)

    def find_books(self, query=None):
        if query is None:
            query = {}
        return list(self.books_collection.find(query))
    
    def check_admin_credentials(self, username, password):
        admin = self.find_one_admin({"username": username})
        if admin:
            hashed_password = admin['password']
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        return False