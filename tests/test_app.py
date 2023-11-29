import pytest
from flask import jsonify
import json

from main import app




@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_login(client):
    response = client.post('/login', json={"username": "user1", "password": "hashed_password_1"})
    assert response.status_code == 200
    assert 'access_token' in response.json


def test_protected_route(client):
    response = client.get('/protected')
    assert response.status_code == 401  # Unauthorized, as we didn't provide a token

    # Log in to get a token
    login_response = client.post('/login', json={"username": "user1", "password": "hashed_password_1"})
    token = login_response.json['access_token']

    # Access protected route with the obtained token
    response = client.get('/protected', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert 'logged_in_as' in response.json


def test_upload_file(client):
    response = client.post('/upload')
    assert response.status_code == 401  # Unauthorized, as we didn't provide a token

    # Log in to get a token
    login_response = client.post('/login', json={"username": "user1", "password": "hashed_password_1"})
    token = login_response.json['access_token']

    # Access upload_file route with the obtained token
    response = client.post('/upload', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.get_data(as_text=True) == 'file uploaded successfully'


def test_get_available_files(client):
    response = client.get('/available_files')
    assert response.status_code == 401

    login_response = client.post('/login', json={"username": "user1", "password": "hashed_password_1"})
    token = login_response.json['access_token']

    response = client.get('/available_files', headers={'Authorization': f'Bearer {token}'})
    response_data = response.json
    assert response.status_code == 200
    assert response_data['data'][0]['name'] == 'image1.jpg'
    assert response_data['data'][1]['name'] == 'image2.jpg'
    assert response_data['data'][2]['name'] == 'image3.jpg'
