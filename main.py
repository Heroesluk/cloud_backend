from flask import Flask, render_template, request, send_from_directory, abort, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "jakis_sobie_tajnyklucz"
jwt = JWTManager(app)

available_files = []


def check_credentials(username: str, password: str):
    # here we should call DB to check if username and password match
    # ex: result: boolean = check(username,password) and return false
    # since we don't have db for now it will always return true
    return True


def generate_access_token(username):
    return create_access_token(identity=username)


def get_user_files(username: str):
    # here based on query with username to the db we should return user_files json
    # which could look like:
    # { username: "name", files: [{filename:"filename1.jpg",
    # directory: "directory", size: 1000}, {filename: ... }] }

    return {}


def save_to_blob_storage(file):
    # here we will save the file to the external storage
    return True


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

    if check_credentials(username, password):
        access_token = create_access_token(identity=username)
    else:
        return jsonify({"msg": "Bad username or password"}), 401

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
    files = get_user_files(current_user)

    return jsonify(files), 200


# Endpoint do przesyłania plików
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()

    save_to_blob_storage(None)

    # f = request.files['file']
    # f.save(secure_filename(f.filename))
    # available_files.append(f.filename)

    return 'file uploaded successfully'


if __name__ == '__main__':
    app.run(debug=True)
