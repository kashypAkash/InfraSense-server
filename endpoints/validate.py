from flask import Blueprint, jsonify
from flask_restful import reqparse, Resource, Api, marshal_with, marshal, fields
from models.models import User

user_fields = {
    'username': fields.String,
    'email':fields.String,
    'password':fields.String,
    'is_admin':fields.Boolean
}

class Login(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])
        self.reqparse.add_argument('password', required=True, help='password is required', location=['form','json'])
        self.reqparse.add_argument('email', required=True, help='email is required', location=['form','json'])


    def get(self):
        users = [marshal(user,user_fields) for user in User.select()]
        return {'users':users}

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        user = User.create(**args)
        return user


login_api = Blueprint('resources.validate', __name__)

api = Api(login_api)
api.add_resource(Login, '/api/v1/validate', endpoint='login')
api.add_resource(Login, '/api/v1/register', endpoint='register')

