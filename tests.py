import unittest
from flask import Flask
from flask_testing import TestCase
from your_app_file import app, db, User

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_users(self):
        response = self.client.get('/users')
        self.assert200(response)
        self.assertEqual(response.json, [])

    def test_handle_user_get(self):
        user = User(username='test_user', email='test@example.com')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/user/{user.id}')
        self.assert200(response)
        self.assertEqual(response.json, {'id': user.id, 'username': user.username, 'email': user.email})

    def test_handle_user_post(self):
        data = {'username': 'new_user', 'email': 'new_user@example.com'}
        response = self.client.post('/user/1', json=data)
        self.assert200(response)
        self.assertEqual(response.json, {'message': 'User updated successfully'})

    def test_handle_user_put(self):
        data = {'username': 'updated_user', 'email': 'updated_user@example.com'}
        response = self.client.put('/user/1', json=data)
        self.assert200(response)
        self.assertEqual(response.json, {'message': 'User updated successfully'})

if __name__ == '__main__':
    unittest.main()
