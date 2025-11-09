# models.py
# from pymongo import MongoClient
from . import db
from datetime import datetime, timezone
import hashlib
import os

# client = MongoClient("mongodb://localhost:27017/")
# db = client["artist_chat"]



# You can store this securely in your environment variables
SECRET_SALT = os.getenv("SECRET_SALT", "default_salt_for_dev")

def make_trip_id(username: str, trip_secret: str) -> str:
    """Generate a short unique tripcode-like ID for user identity."""
    s = f"{username}:{trip_secret}:{SECRET_SALT}"
    h = hashlib.sha256(s.encode()).hexdigest()
    return h[:10]

def hash_ip(ip: str) -> str:
    """Store hashed IP (for privacy)."""
    return hashlib.sha256(ip.encode()).hexdigest()

def save_message(username, trip_secret, text, ip= None):
    """Save chat message to MongoDB."""
    trip_id = make_trip_id(username, trip_secret) if trip_secret else None
    ip_hash = hash_ip(ip)
    message = {
        "username": username or "Guest",
        "trip_id": trip_id,
        "message": text,
        "timestamp": datetime.now(timezone.utc),
        "ip_hash": ip_hash,
    }
    result = db.messages.insert_one(message)
    message["_id"] = str(result.inserted_id)
    return message

def create_admin(username, password_hash):
    """Create admin record (you’ll run this once manually)."""
    admin = {"username": username, "password_hash": password_hash}
    db.admin.insert_one(admin)
