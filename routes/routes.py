# Import necessary modules
from flask import jsonify, request
from app import app
import requests

USUARIO_ANONIMO = 'gsierram'
PASSWORD_ANONIMO = 'FalsoPassword$%'
url_servidor = 'https://devsys.iingen.unam.mx/geco3/'

# Route to retrieve all items
@app.route('/api/login', methods=['POST'])
def create_item():
    try:
        url = url_servidor+'proyectos/apidocs/get-token'
        data = {
        'username': USUARIO_ANONIMO,
        'password': PASSWORD_ANONIMO,
        }
        response = requests.post(url, data=data)

        return response.json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Route to retrieve all items
@app.route('/api/get_corpus/<int:corpus_id>', methods=['GET'])
def get_items(corpus_id):
    try:
        authorization_header = request.headers.get('Authorization')
        
        parts = authorization_header.split()
        url = url_servidor+f'proyectos/apidocs/corpus/{corpus_id}'
        headers = {'Authorization': 'Token ' + parts[1]}
        response = requests.get(url, headers=headers )
        return response.json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
