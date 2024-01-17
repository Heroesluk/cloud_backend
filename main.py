import datetime
import os
import zipfile

from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.utils import secure_filename

from dbConnection import match_credentials_query, get_user_id_query, get_user_files_query, get_user_by_username_query, \
    add_user_to_db, add_image_data_to_db, delete_image_from_db, get_image_by_id, add_log_entry
from fileManagement import get_signed_urls_for_user, upload_file_to_bucket, remove_image_from_cache, \
    delete_image_from_storage
from models import User, Image, LogEntry

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

app.config["JWT_SECRET_KEY"] = "jakis_sobie_tajnyklucz"
jwt = JWTManager(app)

available_files = []
# stores k,v pair where key is token and value is user id
access_token_users_dict = {}

bucket_storage = 'cloud_image_bucket'


def generate_access_token(username):
    return create_access_token(identity=username)


def get_user_files(user_id: int):
    return get_user_files_query(user_id)


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if match_credentials_query(username, password):
        access_token = create_access_token(identity=username)
        id = get_user_id_query(username)
        access_token_users_dict[access_token] = id
    else:
        add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "User {} failed login attempt".format(username)))

        return jsonify({"msg": "Bad username or password"}), 401

    add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "User {} logged in".format(username)))
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
# @app.route('/available_files', methods=['GET'])
# @jwt_required()
# def get_available_files():
#     current_user = get_jwt_identity()
#     images = get_user_files(get_user_id_query(current_user))
#     get_signed_urls_for_user(bucket_storage,[str(i.folder_id) for i in images])
#     return jsonify(data=[e.serialize() for e in files]), 200


@app.route('/available_files', methods=['GET'])
@jwt_required()
def get_available_files():
    current_user = get_jwt_identity()
    images = get_user_files(get_user_id_query(current_user))
    images_with_urls = get_signed_urls_for_user(bucket_storage, images)

    add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "User {} requested images".format(current_user)))

    return jsonify(data=[e.serialize() for e in images_with_urls]), 200


# Endpoint do przesyłania plików
@app.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    current_user = get_jwt_identity()

    file_data = request.files['file']
    filename = secure_filename(file_data.filename)
    file_data.save(filename)

    try:
        to_return = ''
        with zipfile.ZipFile(filename, 'r') as zip_ref:
            # Assuming all files are images
            for file_info in zip_ref.infolist():
                
                unzipped = secure_filename(file_info.filename)
                with zip_ref.open(file_info.filename) as source, open(unzipped, 'wb') as target:
                    target.write(source.read())

                size = os.path.getsize(unzipped)
                img = Image(0, unzipped, get_user_id_query(current_user),
                            size, datetime.datetime.now())
                add_image_data_to_db(img)

                link = upload_file_to_bucket(bucket_storage, unzipped, img.get_bucket_path())
                to_return = link if to_return == '' else ''

                os.remove(unzipped)
                
                add_log_entry(
                    LogEntry(1, "INFO", datetime.datetime.now(), "User {} uploaded file {}".format(current_user, unzipped)))

        os.remove(filename)
        return str(to_return)
    except Exception as e:
        pass

    size = os.path.getsize(filename)

    img = Image(0, filename, get_user_id_query(current_user),
                size, datetime.datetime.now())

    add_image_data_to_db(img)
    link = upload_file_to_bucket(bucket_storage, filename, img.get_bucket_path())
    os.remove(filename)

    add_log_entry(
        LogEntry(1, "INFO", datetime.datetime.now(), "User {} uploaded file {}".format(current_user, img.name)))

    return str(link)

@app.route('/', methods=['GET'])
def test():
    return "true", 200


@app.route('/tokens', methods=['GET'])
def test2():
    return access_token_users_dict


@app.route("/register", methods=["POST"])
def register():
    user_data = request.json

    try:
        # Check if the user exists
        existing_user = get_user_by_username_query(user_data["username"])
        if existing_user:
            return jsonify({"msg": f"user {str(existing_user.username)} already exists"}), 400

        # If the user doesn't exist then
        new_user = User(
            0,
            username=user_data["username"],
            password=user_data["password"],
            email=user_data["email"]
        )

        add_user_to_db(new_user)
    except Exception as e:
        print(e)
        add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "Could not register new user"))

        return jsonify({"msg": "Error during user registration"}), 500

    add_log_entry(
        LogEntry(1, "INFO", datetime.datetime.now(), "User {} registered successfully".format(user_data["username"])))

    return jsonify({"msg": "User registered successfully"}), 200


@app.route('/delete_image', methods=['POST'])
@jwt_required()
@cross_origin(origin='http://localhost:5173', methods=['POST', 'DELETE'], supports_credentials=True)
def delete_image():
    current_user = get_jwt_identity()
    image_id = request.json.get('image_id', None)

    image = get_image_by_id(image_id)
    if not image or image.folder_id != get_user_id_query(current_user):
        add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "Image not found or unauthorized".format(image.name)))

        return jsonify({"msg": "Image not found or unauthorized"}), 404

    delete_image_from_db(image_id)

    remove_image_from_cache(image_id)

    delete_image_from_storage(bucket_storage, image.get_bucket_path())

    add_log_entry(LogEntry(1, "INFO", datetime.datetime.now(), "Image {} deleted successfully".format(image.name)))

    return jsonify({"msg": "Image deleted successfully"}), 200

@app.route('/docs')
def swagger_ui():
    return render_template('swagger_ui.html')


@app.route('/spec')
def get_spec():
    return send_from_directory(app.root_path, 'openapi.yaml')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
