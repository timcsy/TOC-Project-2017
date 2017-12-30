from config import *

from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
db = client['test']
db.inventory.insert_one(
    {"item": "canvas",
     "qty": 100,
     "tags": ["cotton"],
     "size": {"h": 28, "w": 35.5, "uom": "cm"}})
print(db.inventory.find_one({"item": "canvas"}))