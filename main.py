import os

from flask import Flask, render_template, request, send_from_directory, abort, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from dbConnection import match_credentials_query, get_user_id_query, get_user_files_query
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

app.config["JWT_SECRET_KEY"] = "jakis_sobie_tajnyklucz"
jwt = JWTManager(app)

available_files = []
access_tokens = {}

def generate_access_token(username):
    return create_access_token(identity=username)


def get_user_files(user_id: int):
    return get_user_files_query(user_id)


def save_to_blob_storage(file):
    # here we will save the file to the external storage
    return True


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if match_credentials_query(username, password):
        access_token = create_access_token(identity=username)
        id = get_user_id_query(username)
        access_tokens[access_token] = id
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


# Endpoint do pobierania dostępnych plików
@app.route('/available_files', methods=['GET'])
@jwt_required()
def get_available_files():
    current_user = get_jwt_identity()
    files = get_user_files(get_user_id_query(current_user))
    return jsonify(data=[e.serialize() for e in files]), 200


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


@app.route('/', methods=['GET'])
def test():
    return "true", 200


@app.route('/tokens', methods=['GET'])
def test2():
    return access_tokens


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
