import os
import sys
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir_of_module = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir_of_module)

import pytest
from backend.app import create_app as backend_create_app
from dataanalyzer.app import create_app as analyzer_create_app 
import json

@pytest.fixture
def backend_client():
    app = backend_create_app()
    app.config['TESTING'] = True

    with app.test_client() as backend_client:
        yield backend_client

def test_welcome_endpoint(backend_client):
    response = backend_client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Welcome to Fitness Buddy Backend!'

@pytest.fixture
def analyzer_client():
    app = analyzer_create_app()
    app.config['TESTING'] = True

    with app.test_client() as analyzer_client:
        yield analyzer_client

def test_index_endpoint(analyzer_client):
    response = analyzer_client.get('/')
    assert response.status_code == 200
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200

    # Check if the response data matches the expected output
    assert response.data == b"Flask app running."
