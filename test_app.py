import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_sqlalchemy import SQLAlchemy

from app import app, db, User

@pytest.fixture
def client():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://1234:7890@db:3306/db_name'

    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

@pytest.fixture
def sample_user():
    return {'name': 'John Doe'}

def test_add_user(client, sample_user):
    response = client.post('/user', json=sample_user)
    assert response.status_code == 201

    users = User.query.all()
    assert len(users) == 1
    assert users[0].name == sample_user['name']

def test_get_users(client, sample_user):
    client.post('/user', json=sample_user)

    response = client.get('/users')
    assert response.status_code == 200

    data = response.json
    assert len(data) == 1
    assert data[0]['name'] == sample_user['name']
