from flask import Flask, request, jsonify, render_template
from models.models import db, save_message
from werkzeug.security import generate_password_hash, check_password_hash

# app.register_blueprint(auth_bp)

app = Flask(__name__)

#mongodb connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/artist_chat"
# mongo.init_app(app)

@app.route('/')
def home():
    return render_template("index.html")
@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/admin')
def admin():
    return render_template('admin.html')

#chat routes
@app.route("/chat/send", methods=["POST"])
def send_message():
    data = request.get_json()
    username = data.get("username", "Guest")
    trip_secret = data.get("tripcode", None)
    text = data.get("message", "")
    ip = request.remote_addr

    if not text.strip():
        return jsonify({"error":"what are you trying to do sending an empty message?"}), 400
    
    message = save_message(username, trip_secret, text, ip)
    return jsonify({"message": "sent", "data": message}), 201

@app.route("/chat/get", methods=["GET"])
def get_messages():
    """fetch latest messages"""
    messages = list(db.messages.find().sort("timestamp").limit(50))
    for m in messages:
        m["_id"] = str(m["_id"])
        m["tripcode"] = m.get("tripcode", "")
    return jsonify(messages), 200


#admin routes
@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    admin = db.admin.find_one({"username": username})
    if not admin or not check_password_hash(admin["password_hash"], password):
        return jsonify({"error": "invalid"}), 401
    
    return jsonify({"message": "admin logged in"}), 200


if __name__ == "__main__":
    app.run(debug=True)



# app = Flask(__name__)
# #connect to mongodb
# client = MongoClient("mongodb://localhost:27017/")
# db = client["artist_website"] #connects to artist_website_db


# @app.route('/')
# def home():
#     return jsonify({"message": "Artist website API is running!"})

# # Example route to insert a test document
# @app.route('/test_insert', methods=['POST'])
# def test_insert():
#     data = request.get_json()
#     result = db.test_collection.insert_one(data)

# #attach string version of the inserted _id to the response
#     data["_id"] = str(result.inserted_id)

#     return jsonify({"status": "success", "data": data}), 201

# if __name__ == '__main__':
#     app.run(debug=True)
