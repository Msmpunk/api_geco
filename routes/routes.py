# Import necessary modules
from flask import jsonify, request
from app import app
import requests
import json

USUARIO_ANONIMO = 'gsierram'
PASSWORD_ANONIMO = 'FalsoPassword$%'
url_servidor = 'http://devsys.iingen.unam.mx/geco4/'

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
        JSONdocsCorpus = response.json()
        print(f'Obtenemos el documento {JSONdocsCorpus["data"][0]}')

        for numero in JSONdocsCorpus["data"]:
            get_items(corpus_id, numero["id"], parts[1])
            print(numero["id"])
        return response.json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def get_items(id_corpus, id_doc, token):
    print(id_corpus, id_doc, token)
    url = url_servidor + f'proyectos/apidocs/corpus/{id_corpus}/{str(id_doc)}/pos'
    headers = {'Authorization': 'Token ' + token}  
    response = requests.get(url, headers=headers) 
    if response.status_code == 200:                
        JSONdocsCorpus = response.json()           
        file_path = f'{11444444}.txt'  # Ajuste para usar f-string
        with open(file_path, 'a') as file:
            # Escribe el JSON en el archivo de texto
            json.dump(JSONdocsCorpus["data"], file, ensure_ascii=False)
            file.write('\n\n')  # Agrega dos líneas nuevas después del JSON