from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_session import Session
import os
from werkzeug.utils import secure_filename
from alg_runner import AlgRunner

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/research-db"
app.config["SECRET_KEY"] = "your-secret-key"
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

CORS(app, supports_credentials=True)
Session(app)
mongo = PyMongo(app)

# Research Model
def get_research_collection():
    return mongo.db.research

# File upload handler
def save_file(file):
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return filepath
    return None

# Research Routes
@app.route("/api/research", methods=["POST"])
def create_research():
    try:
        AlgRunner().runner()
        file1 = request.files.get("file1")
        file2 = request.files.get("file2")
        
        file1_path = save_file(file1)
        file2_path = save_file(file2)
        
        research_data = {
            "userId": 111,  # Replace with session user ID when authentication is implemented
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "category": request.form.get("category"),
            "notes": request.form.get("notes"),
            "file1Path": file1_path,
            "file2Path": file2_path,
            "createdAt": mongo.db.command("serverStatus")["localTime"]
        }
        research_id = get_research_collection().insert_one(research_data).inserted_id
        return jsonify({"message": "Research data saved successfully!", "id": str(research_id)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/research", methods=["GET"])
def get_research():
    try:
        research_list = list(get_research_collection().find({"userId": 111}))  # Replace with session user ID
        for research in research_list:
            research["_id"] = str(research["_id"])
        return jsonify(research_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=3000, debug=True)
