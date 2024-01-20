import pytest
import json
from unittest.mock import patch, MagicMock
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@patch('app.SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
def test_get_all_users(client):
    mock_query = MagicMock()
    mock_query.all.return_value = [
        User(id=1, name='User1'),
        User(id=2, name='User2')
    ]
    with patch('app.User.query', mock_query):
        response = client.get('/users')
        data = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert isinstance(data, list)
        assert len(data) == 2

@patch('app.SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
def test_add_user(client):
    user_data = {'name': 'John Doe'}
    response = client.post('/users', json=user_data)
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data['message'] == 'User added successfully'

@patch('app.SQLALCHEMY_DATABASE_URI', 'sqlite:///:memory:')
def test_get_user(client):
    user = User(name='Test User')
    with patch('app.User.query.get_or_404', return_value=user):
        response = client.get('/user/1')
        data = json.loads(response.data.decode('utf-8'))

        assert response.status_code == 200
        assert data['name'] == 'Test User'
