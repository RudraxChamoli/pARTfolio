from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URI)
db = client["artist_website_db"]

# from .models import save_message, get_messages