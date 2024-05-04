import os
import sys
import pytest
import json

from backend.app import create_app as backend_create_app
from dataanalyzer.app import create_app as analyzer_create_app
from unittest.mock import patch, MagicMock
from backend.app import create_app
from datetime import datetime

from flask import Flask

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir_of_module = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir_of_module)

# Successful request: assert response.status_code == 200


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(app_routes)
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


# Integration Test Method 1
def test_workouts_endpoint(client):
    response = client.get('/workouts')

    assert response.status_code == 200

    assert response.data

# Integration Test Method 2
def test_sign_up_endpoint(client):

    # Define sample signup data
    sample_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }

    # Send POST request to '/sign_up' endpoint with sample_data
    response = client.post('/sign_up', json=sample_data)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200

    # Assert that the response contains the expected message and username
    assert response.json['message'] == 'Logged in'
    assert response.json['username'] == sample_data['username']


# Integration Test Method 3
def test_view_progress_endpoint(client):
    # Define sample username
    sample_username = 'testuser'

    # Send GET request to '/progress' endpoint w/ sample username
    response = client.get('/progress?username=' + sample_username)

    # Check if request was successful
    assert response.status_code == 200

    # Assert response contains expected data
    assert response.json == [
        {'username': sample_username, 'progress': 'some_data'}]  # Adjust based on the expected response data

# # Integration Test Method  4
def test_view_progress_endpoint_no_username(client):
    # Send a GET request to the '/progress' endpoint without a username
    response = client.get('/progress')

    # Check if the response status code is 400 (Bad Request)
    assert response.status_code == 400

    # Assert that the response contains the expected error message
    assert response.json == {'error': 'Username is required'}

# Integration Test Method 5
def test_view_progress_endpoint_wrong_method(client):
    # Send a POST request to the '/progress' endpoint
    response = client.post('/progress')

    # Check if the response status code is 405 (Method Not Allowed)
    assert response.status_code == 405

    # Assert that the response contains the expected error message
    assert response.json == {'error': 'must be GET'}