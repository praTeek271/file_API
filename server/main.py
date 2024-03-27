import os
from flask import Flask, request, jsonify, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
import hashlib

app_flask = Flask(__name__)
auth = HTTPBasicAuth()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app_flask.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

USERNAME = 'admin'
PASSWORD = '72password'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hash_password(password):
    # Hash the password using SHA-256
    return hashlib.sha256(password.encode()).hexdigest()

@auth.verify_password
def verify_password(username, password):
    # Verify the password
    return username == USERNAME and hash_password(password) == hash_password(PASSWORD)

@app_flask.route('/upload', methods=['POST'])
# @auth.login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            folder_path = os.path.join(app_flask.config['UPLOAD_FOLDER'], request.form.get('name'))
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, filename)
            file.save(file_path)
        except Exception as e:
            return jsonify({'error': "Failed to upload file", 'exception': str(e)})
        
        # Generate a token (in this example, using filename)
        token = request.form.get('token')

        # Generate download link
        download_link = url_for('download_file', filename=filename, _external=True)

        return jsonify({'success': 'File uploaded successfully', 'filename': filename, 'token': token, 'download_link': download_link})
    else:
        return jsonify({'error': 'Invalid file format'})

@app_flask.route('/')
@auth.login_required
def index():
    folders = os.listdir('uploads')
    return render_template('index.html', folders=folders)

@app_flask.route('/files/<folder_name>')
@auth.login_required
def show_files(folder_name):
    folder_path = os.path.join('uploads', folder_name)
    if os.path.exists(folder_path):
        files = os.listdir(folder_path)
        return render_template('folder.html', folder_name=folder_name, files=files)
    else:
        return jsonify({'error': 'Folder not found'}), 404

@app_flask.route('/download/<filename>')
@auth.login_required
def download_file(filename):
    from flask import send_file
    # Provide a download link to the file
    # file_path = os.path.join(UPLOAD_FOLDER, filename)
    file_path = os.path.join(UPLOAD_FOLDER, 'jarqq\file1_copy_2.txt')
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app_flask.run(debug=True)




# # # __Notes__:
#  https://stackoverflow.com/questions/61824774/uploading-and-processing-files-with-flask-rest-api
