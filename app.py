from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import time

time.sleep(10)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pesho:12345@db:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.route('/')
def home():
    return jsonify({'message': 'API HOME'})

@app.route('/users', methods=['GET'])                                                                                           
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

@app.route('/user/<int:user_id>', methods=['GET', 'POST', 'PUT'])
def handle_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

    if request.method == 'POST':
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

    if request.method == 'PUT':
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0')
