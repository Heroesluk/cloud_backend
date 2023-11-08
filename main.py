from flask import Flask, render_template, request, send_from_directory, abort, jsonify
import datetime
import jwt
from werkzeug.utils import secure_filename

app = Flask(__name__)

available_files = []

# available_files = {
# ['filename1.jpg', 'filename2.jpg', 'filename3.jpg']
# }


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    available_files.append(f.filename)
    return 'file uploaded successfully'


@app.route('/get_file', methods=['GET'])
def get_file():
    file_name = request.args.get('file_name')
    if file_name:
        try:
            return send_from_directory('', file_name)
        except FileNotFoundError:
            abort(400)
    else:
        return


@app.route('/available_files', methods=['GET'])
def get_available_files():
    return jsonify({'available_files': available_files})


if __name__ == '__main__':
    app.run(debug=True)
