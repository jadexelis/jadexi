from flask import Flask
from io import StringIO
import sys

class FlaskLambda(Flask):
    def __call__(self, event, context):
        return self.handler(event, context)

    def handler(self, event, context):
        with self.request_context(self.create_environ(event)):
            try:
                response = self.full_dispatch_request()
            except Exception as e:
                return {
                    'statusCode': 500,
                    'body': str(e)
                }
            
            return {
                'statusCode': response.status_code,
                'headers': dict(response.headers),
                'body': response.get_data(as_text=True)
            }

    def create_environ(self, event):
        environ = {
            'REQUEST_METHOD': event['httpMethod'],
            'SCRIPT_NAME': '',
            'PATH_INFO': event['path'],
            'QUERY_STRING': event['queryStringParameters'] or '',
            'SERVER_NAME': 'localhost',
            'SERVER_PORT': '80',
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': StringIO(event.get('body', '')),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }
        
        headers = event.get('headers', {})
        for key, value in headers.items():
            key = 'HTTP_' + key.upper().replace('-', '_')
            environ[key] = value
            
        return environ 