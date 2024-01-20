from flask_restplus import Api, Resource, fields
from flask import Flask

app = Flask(__name__)
api = Api(app, version='1.0', title='User API', description='API for managing users')

ns = api.namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True, description='The user identifier'),
    'username': fields.String(required=True, description='The username'),
    'email': fields.String(required=True, description='The email address')
})

class UserResource(Resource):
    @api.marshal_with(user_model)
    def get(self, user_id):
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

    @api.expect(user_model)
    def put(self, user_id):
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})

@ns.route('/')
class UserListResource(Resource):
    @api.marshal_list_with(user_model)
    def get(self):
        users = User.query.all()
        return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

    @api.expect(user_model)
    @api.marshal_with(user_model, code=201)
    def post(self):
        data = request.get_json()
        user.username = data['username']
        user.email = data['email']
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
        

if __name__ == '__main__':
    app.run(host='0.0.0.0')
