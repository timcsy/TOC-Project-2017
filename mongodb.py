from config import *
from pymongo import MongoClient

client = MongoClient(MONGODB_URI)
db = client['test']