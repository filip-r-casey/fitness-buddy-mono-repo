import pytest
from unittest.mock import patch, MagicMock
from backend.app import create_app  
from datetime import datetime


@pytest.fixture 
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

@patch('backend.app.views.psycopg2.connect')
def test_workouts_success(mock_connect, client):
    mock_cursor = MagicMock()
    return_value = [{'id': 1, 'name': 'Workout 1'}, {'id': 2, 'name': 'Workout 2'}]
    mock_cursor.fetchall.return_value = return_value
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    response = client.get('/workouts?name=test')
    assert response.status_code == 200
    data = response.json
    assert data == return_value

# Test case for the sign_up endpoint
@patch('backend.app.views.psycopg2.connect')  
def test_sign_up(mock_connect, client):
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    json_data = {
        'username': 'test_user',
        'email': 'test@example.com',
        'password': 'test_password'
    }
    response = client.post('/sign_up', json=json_data)
    mock_cursor.execute.assert_called_once_with(
        "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
        ('test_user', 'test@example.com', 'test_password')
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data == {'message': 'Logged in', 'username': 'test_user'}

@patch('backend.app.views.psycopg2.connect')  
def test_add_progress(mock_connect, client):
  
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    json_data = {
        'user': 'test_user',
        'workout_name': 'test_workout',
        'date': datetime.now().timestamp(),
        'reps': 10,
        'sets': 3,
        'weight': 50
    }

    response = client.post('/add_progress', json=json_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data == {'message': 'record created'}

