import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_id = os.path.splitext(filename)[0]
        resp = jsonify({'message' : f'File {file_id} successfully uploaded' })
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route("/file/<id>", methods=["GET"])
def file(id):
    for root, dir, file in os.walk(app.config['UPLOAD_FOLDER']):
        for name in file:
            if id in name:
                print(file)
                resp = jsonify({'message' : f'File {id} was found'})
                resp.status_code = 200
                resp.file = name
                return send_file(os.path.join(app.config["UPLOAD_FOLDER"], name))
        
    resp = jsonify({'message' : f'File {id} was not found'})
    resp.status_code = 400
    return resp



if __name__ == "__main__":
    app.run()