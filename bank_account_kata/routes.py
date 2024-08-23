from flask import Flask, request, jsonify
from models import db, Account, Transaction

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

@app.route('/accounts', methods=['POST'])
def create_account():
    data = request.get_json()
    account = Account(name=data['name'], balance=data.get('balance', 0.0))
    db.session.add(account)
    db.session.commit()
    return jsonify({'id': account.id, 'name': account.name, 'balance': account.balance}), 201

@app.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    account = Account.query.get_or_404(account_id)
    return jsonify({'id': account.id, 'name': account.name, 'balance': account.balance})

@app.route('/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = Account.query.get_or_404(account_id)
    db.session.delete(account)
    db.session.commit()
    return '', 204

@app.route('/accounts/<int:account_id>/deposit', methods=['POST'])
def deposit(account_id):
    data = request.get_json()
    amount = data['amount']
    account = Account.query.get_or_404(account_id)
    account.balance += amount
    transaction = Transaction(account_id=account_id, type='deposit', amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'id': transaction.id, 'type': transaction.type, 'amount': transaction.amount, 'date': transaction.date}), 201

@app.route('/accounts/<int:account_id>/withdraw', methods=['POST'])
def withdraw(account_id):
    data = request.get_json()
    amount = data['amount']
    account = Account.query.get_or_404(account_id)
    if account.balance < amount:
        return jsonify({'error': 'Insufficient funds'}), 400
    account.balance -= amount
    transaction = Transaction(account_id=account_id, type='withdraw', amount=amount)
    db.session.add(transaction)
    db.session.commit()
    return jsonify({'id': transaction.id, 'type': transaction.type, 'amount': transaction.amount, 'date': transaction.date}), 201

@app.route('/accounts/<int:account_id>/transactions', methods=['GET'])
def get_transactions(account_id):
    transactions = Transaction.query.filter_by(account_id=account_id).all()
    return jsonify([{'id': t.id, 'type': t.type, 'amount': t.amount, 'date': t.date} for t in transactions])

if __name__ == '__main__':
    app.run(debug=True)
