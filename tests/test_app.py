# tests/conftest.py
import json
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app()
    flask_app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })

    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    db.create_all()  # create table

    yield testing_client  

    db.session.remove()
    db.drop_all()
    ctx.pop()

# tests/test_auth.py
def test_registration(test_client):
    """test register"""
    response = test_client.post('/api/register', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword',
        'email': 'abc@gmail.com'
    }), content_type='application/json')
    assert response.status_code == 201

def test_login_and_logout_flow(test_client):
    # login
    login_response = test_client.post('/api/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
    assert login_response.status_code == 200

    # go index
    index_response = test_client.get('/api/index')
    assert index_response.status_code == 200

    # logout
    logout_response = test_client.post('/api/logout', follow_redirects=True)
    assert logout_response.status_code == 200
    assert 'api/login' in logout_response.json['redirect'], "Should redirect to the login page"


#test unauthorized_access after logout
def test_unauthorized_access_redirects_to_login(test_client):
    """test unauthorized access"""
    response = test_client.get('/api/index', follow_redirects=True)
    assert b"Login" in response.data  