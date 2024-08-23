import pytest
from app import app, db, Account, Transaction

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

def test_deposit(client):
    client.post('/accounts', json={'name': 'John Doe'})
    response = client.post('/accounts/1/deposit', json={'amount': 100.0})
    assert response.status_code == 201
    data = response.get_json()
    assert data['amount'] == 100.0

def test_withdraw(client):
    client.post('/accounts', json={'name': 'John Doe', 'balance': 100.0})
    response = client.post('/accounts/1/withdraw', json={'amount': 50.0})
    assert response.status_code == 201
    data = response.get_json()
    assert data['amount'] == 50.0

def test_withdraw_insufficient_funds(client):
    client.post('/accounts', json={'name': 'John Doe'})
    response = client.post('/accounts/1/withdraw', json={'amount': 50.0})
    assert response.status_code == 400
    data = response.get_json()
    assert data['error'] == 'Insufficient funds'
