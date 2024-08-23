import pytest
from app import app, db, Account

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_account(client):
    response = client.post('/accounts', json={'name': 'John Doe'})
    assert response.status_code == 201
    data = response.get_json()
    assert data['name'] == 'John Doe'

def test_get_account(client):
    client.post('/accounts', json={'name': 'John Doe'})
    response = client.get('/accounts/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Doe'
