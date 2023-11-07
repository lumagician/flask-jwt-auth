from config import app, db, api

from flask_restful import Resource
from flask_restful.reqparse import RequestParser
import uuid

import os
import bcrypt

from models import User

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager

class Signup(Resource):
    """
    example signup url: http://127.0.0.1:5000/signup
    """
    def get(self):
        parser = RequestParser()
        parser.add_argument('username', required=True, help="username is required")
        parser.add_argument('password', required=True, help="password is required")
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        # check if username already exists
        user = User.query.filter_by(username=username).first()
        if user:
            return {"message": "Username already exists"}, 400
        

        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt(12)
        hash = bcrypt.hashpw(password_bytes, salt)

        salt_b64 = salt.decode('utf-8')
        user = User(str(uuid.uuid4()), username, hash, salt_b64)
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

class Login(Resource):
    """
    example login url: http://127.0.0.1:5000/login
    """
    def post(self):
        parser = RequestParser()
        parser.add_argument('username', required=True, help="username is required")
        parser.add_argument('password', required=True, help="password is required")
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "Credentials do not match"}, 404
        
        password_bytes = password.encode('utf-8')
        salt_b64 = user.salt
        salt = salt_b64.encode('utf-8')
        
        if bcrypt.hashpw(password_bytes, salt) != user.password_hash:
            return {"message": "Incorrect password"}, 401
        
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token}, 200

class SecretResource(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        print(current_user + " is logged in")

        return {"answer": 42}



api.add_resource(Login, '/login')
api.add_resource(SecretResource, '/secret')
api.add_resource(Signup, '/signup')

if __name__ == '__main__':
    app.run(debug=True)
