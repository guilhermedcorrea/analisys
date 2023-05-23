from flask import Blueprint, redirect, render_template,current_app,request, redirect, url_for, abort, send_from_directory   
import imghdr
import os
from werkzeug.utils import secure_filename


from .uploads import UploadFiles

Admin = Blueprint("analytics",__name__)
import base64


@Admin.route('/')
def index():
    """Teste Upload"""
    files = os.listdir(current_app.config['UPLOAD_PATH'])
    return render_template('upload.html', files=files)


@Admin.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in current_app.config['UPLOAD_EXTENSIONS']:
            return "Invalid image", 400
        uploaded_file.save(os.path.join(current_app.config['UPLOAD_PATH'], filename))
        upload_files = UploadFiles(os.path.join(os.path.join(current_app.config['UPLOAD_PATH'], filename)))
        upload_files.reader_files()
        
    return '', 204


@Admin.route('/uploads/<filename>')
def upload(filename): 
    return send_from_directory(current_app.config['UPLOAD_PATH'], filename)


@Admin.route('/variavel/lista')
def seleciona_variavel():
    language = request.args.get('variavel')
    if language !=None:
        print(language)
    
    