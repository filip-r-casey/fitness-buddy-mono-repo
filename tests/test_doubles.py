import os
import sys
sys.path.append('/path/to/parent_directory_of_module')
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir_of_module = os.path.abspath(os.path.join(script_dir, '..'))
sys.path.append(parent_dir_of_module)

import pytest
from unittest.mock import patch, MagicMock
from backend.app import create_app  


@pytest.fixture 
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@patch('backend.app.views.psycopg2.connect')
def test_workouts_success(mock_connect, client):
    # Mock psycopg2.connect
    
    mock_cursor = MagicMock()
    return_value = [{'id': 1, 'name': 'Workout 1'}, {'id': 2, 'name': 'Workout 2'}]
    mock_cursor.fetchall.return_value = return_value
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Make request to /workouts endpoint
    response = client.get('/workouts?name=test')

    # Assert response status code
    assert response.status_code == 200

    # Assert response data
    data = response.json
    print(data)
    assert data == return_value