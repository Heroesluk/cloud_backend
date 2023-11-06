from flask import Flask, render_template, request, send_from_directory, abort
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/upload')
def upload_page():
    return render_template('upload.html')


@app.route('/uploader', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(secure_filename(f.filename))
    return 'file uploaded successfully'


@app.route('/get_file', methods=['GET'])
def get_file():
    file_name = request.args.get('file_name')
    if file_name:
        try:
            return send_from_directory('', file_name)
        except FileNotFoundError:
            abort(404)
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
