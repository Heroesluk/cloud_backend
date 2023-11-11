from flask import Flask, render_template, request, send_from_directory, abort, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename

app = Flask(__name__)


app.config["JWT_SECRET_KEY"] = "jakis_sobie_tajnyklucz"
jwt = JWTManager(app)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    try:
        username = request.json["username"]
        password = request.json["password"]
    # username = request.json.get("username", None)
    # password = request.json.get("password", None)
    except KeyError:
        return jsonify({"msg": "Missing username or password in JSON"}), 400
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


available_files = []


# Endpoint do pobierania dostępnych plików
@app.route('/available_files', methods=['GET'])
@jwt_required()
def get_available_files():
    current_user = get_jwt_identity()
    if current_user != 'user1':
        return jsonify({'error': 'Unauthorized'}), 403

    return jsonify({'available_files': available_files}), 200


# Endpoint do przesyłania plików
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()
    if current_user != 'user1':
        return jsonify({'error': 'Unauthorized'}), 403

    f = request.files['file']
    f.save(secure_filename(f.filename))
    available_files.append(secure_filename(f.filename))
    return 'file uploaded successfully'


# Endpoint do wyświetlania strony upload.html
@app.route('/upload_page', methods=['GET'])
@jwt_required()
def upload_page():
    current_user = get_jwt_identity()
    if current_user != 'user1':
        return jsonify({'error': 'Unauthorized'}), 403

    return render_template('upload.html')


# Endpoint do pobierania plików, nie w sumie czy potrzebny
@app.route('/get_file', methods=['GET'])
@jwt_required()
def get_file():
    check_result = check_user_permissions('user1')
    if check_result:
        return check_result

    file_name = request.args.get('file_name')
    if not file_name:
        return jsonify({'error': "Missing file_name parameter"}), 400
    try:
        return send_from_directory('', file_name)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


def check_user_permissions(user):
    current_user = get_jwt_identity()
    if current_user != user:
        return jsonify({'error': 'Unauthorized'}), 403


if __name__ == '__main__':
    app.run(debug=True)
