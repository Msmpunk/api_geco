# Importar los módulos necesarios
from flask import jsonify, request, send_file
from app import app
import requests
import json
import zipfile
import os

# URL del servidor
url_servidor = 'http://www.geco.unam.mx/geco3/'
#url_servidor = 'http://devsys.iingen.unam.mx/geco4/'

# Ruta para crear un ítem
@app.route('/api/login/v1', methods=['POST'])
def create_item():
    try:
        data = request.json

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Falta nombre de usuario o contraseña'}), 400
        
        url = url_servidor+'proyectos/apidocs/get-token'
        payload = {
            'username': data['username'],
            'password': data['password'],
        }

        response = requests.post(url, data=payload)

        return response.json(), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# Ruta para obtener corpus públicos
@app.route('/api/get/corpus_publicos/', methods=['GET'])
def get_corpus():
    try:
        authorization_header = request.headers.get('Authorization')
        
        parts = authorization_header.split()
        
        url = url_servidor+f'proyectos/apidocs/corpus'
        headers = {'Authorization': 'Token ' + parts[1]}
        response = requests.get(url, headers=headers )
        JSONdocsCorpus = response.json()
        
        return JSONdocsCorpus, 200
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# Ruta para obtener un corpus público por su ID
@app.route('/api/get_corpus_publico/<int:corpus_id>', methods=['GET'])
def get_corpus_by_id(corpus_id):
    try:
        authorization_header = request.headers.get('Authorization')
        parts = authorization_header.split()
        url = url_servidor+f'proyectos/apidocs/corpus/{corpus_id}/tabla'
        headers = {'Authorization': 'Token ' + parts[1]}
        response = requests.get(url, headers=headers )
        JSONdocsCorpus = response.json()
        return JSONdocsCorpus, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Ruta para obtener texto
@app.route('/api/get_text/<int:corpus_id>', methods=['POST'])
def get_text(corpus_id):
    try:
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return jsonify({'error': 'Falta el encabezado de autorización'}), 400
        
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            return jsonify({'error': 'Formato de encabezado de autorización inválido'}), 400
                
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Falta el cuerpo de la solicitud o no está en formato JSON'}), 400
 
        for item_doc in data['data']:
            dowload_documents_txt(corpus_id, item_doc, parts[1])

        create_zip_from_folder('texts_files.zip')
        
        zip_filename = "texts_files.zip"
        return send_file(zip_filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        delete_files()

# Ruta para obtener texto con posiciones
@app.route('/api/get_text_pos/<int:corpus_id>', methods=['POST'])
def get_text_pos(corpus_id):
    try:
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return jsonify({'error': 'Falta el encabezado de autorización'}), 400
        
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            return jsonify({'error': 'Formato de encabezado de autorización inválido'}), 400
                
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Falta el cuerpo de la solicitud o no está en formato JSON'}), 400
 
        for item_doc in data['data']:
            dowload_documents_pos(corpus_id, item_doc, parts[1])

        create_zip_from_folder('texts_files_pos.zip')
        
        zip_filename = "texts_files_pos.zip"
        return send_file(zip_filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        delete_files()

# Ruta para obtener texto adjunto
@app.route('/api/get_text_adjuntos/<int:corpus_id>', methods=['POST'])
def get_text_adjuntos(corpus_id):
    try:
        authorization_header = request.headers.get('Authorization')
        
        if not authorization_header:
            return jsonify({'error': 'Falta el encabezado de autorización'}), 400
        
        parts = authorization_header.split()
        if len(parts) != 2 or parts[0].lower() != 'token':
            return jsonify({'error': 'Formato de encabezado de autorización inválido'}), 400
                
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Falta el cuerpo de la solicitud o no está en formato JSON'}), 400
 
        for item_doc in data['data']:
            dowload_documents_adjuntos(corpus_id, item_doc, parts[1])

        create_zip_from_folder('texts_files_adjuntos.zip')
        
        zip_filename = "texts_files_adjuntos.zip"
        return send_file(zip_filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        delete_files()

# Función para descargar documentos de texto
def dowload_documents_txt(corpus_id, doc, token):
    url = url_servidor + f'proyectos/apidocs/corpus/{corpus_id}/{str(doc["id"])}'
    headers = {'Authorization': 'Token ' + token}  
    response = requests.get(url, headers=headers)
    if response.status_code == 200:                
        JSONdocsCorpus = response.json()
        file_name = f'{doc["name"]}'  
        file_path = os.path.join("output_text", file_name)
        with open(file_path, 'a') as file:
            json.dump(JSONdocsCorpus["data"], file, ensure_ascii=False)

# Función para descargar documentos de texto con posiciones
def dowload_documents_pos(corpus_id, doc, token):
    url = url_servidor + f'proyectos/apidocs/corpus/{corpus_id}/{str(doc["id"])}/pos'
    headers = {'Authorization': 'Token ' + token}  
    response = requests.get(url, headers=headers)
    if response.status_code == 200:                
        JSONdocsCorpus = response.json()
        file_name = f'{doc["name"]}'  
        file_path = os.path.join("output_text", file_name)
        with open(file_path, 'a') as file:
            json.dump(JSONdocsCorpus["data"], file, ensure_ascii=False)

# Función para descargar documentos adjuntos
def dowload_documents_adjuntos(corpus_id, doc, token):
    url = url_servidor + f'proyectos/apidocs/corpus/{corpus_id}/{str(doc["id"])}/adjuntos'
    headers = {'Authorization': 'Token ' + token}  
    response = requests.get(url, headers=headers)
    if response.status_code == 200:                
        JSONdocsCorpus = response.json()
        file_name = f'{doc["name"]}'  
        file_path = os.path.join("output_text", file_name)
        with open(file_path, 'a') as file:
            json.dump(JSONdocsCorpus["data"], file, ensure_ascii=False)

# Función para crear un archivo ZIP a partir de una carpeta
def create_zip_from_folder(name):
    folder_path = "output_text"  
    try:
        with zipfile.ZipFile(name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_path)
                    zipf.write(file_path, arcname=arcname)
    except Exception as e:
        print(f"Error al crear el archivo ZIP: {str(e)}")

# Función para eliminar archivos temporales
def delete_files():
    folder_path = "output_text"
    txt_files = [file for file in os.listdir(folder_path) if file.endswith(".txt")]
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        os.remove(file_path)
