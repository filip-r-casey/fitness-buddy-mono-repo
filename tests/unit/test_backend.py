import os
import sys
sys.path.append('/path/to/parent_directory_of_module')
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir_of_module = os.path.abspath(os.path.join(script_dir, '..', '..'))
sys.path.append(parent_dir_of_module)

import pytest
from backend.app import create_app   # Replace this with the correct import
import json

@pytest.fixture
def client():
    app = create_app
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

def test_welcome_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == 'Welcome to Fitness Buddy Backend!'

