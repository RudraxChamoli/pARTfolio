from flask import Blueprint, request, jsonify
from config import db
from models.models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data= request.get_json()
    existing_user = db.users.find_one({"email": data['email']})

    if existing_user:
        return jsonify({"message": "already existing user bozo"}), 400
    
    user = User(data['name'], data['email'], data['password'])
    db.users.insert_one(user.to_dict())

    return jsonify({"message": "registered succ."}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data= request.get_json()
    user_data = db.users.find_one({"email": data['email']})

    if not user_data:
        return jsonify({"message": "no such person"}), 404
    
    user = User(user_data['name'], user_data['email'], user_data['password'])
    if user.verify_password(data['password']):
        return jsonify({"message": "login successful"}), 200
    else:
        return jsonify({"message": "incalid smh"}), 401