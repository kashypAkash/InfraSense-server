from flask import Blueprint, jsonify
from flask_restful import reqparse, Resource, Api, marshal_with, marshal, fields
from models.user import User
from peewee import *

user_fields = {
    'UserName': fields.String,
    'Password':fields.String,
    'EmailId':fields.String
}

class Login(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])
        self.reqparse.add_argument('password', required=True, help='password is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        try:
           if User.get(User.UserName == args['username']).Password == args['password']:
               return jsonify({'statusCode':200,'username':args['username']})
           else:
               return jsonify({'statusCode':400})
        except DoesNotExist:
            return jsonify({'statusCode':400})


class Register(Resource):

    '''This resource is used for  registering a user'''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('UserName', required=True, help='username is required', location=['form','json'])
        self.reqparse.add_argument('Password', required=True, help='password is required', location=['form','json'])
        self.reqparse.add_argument('EmailId', required=True, help='email is required', location=['form','json'])

    @marshal_with(user_fields)
    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        temp_user = User.create(**args)

        return jsonify({'statusCode':200,'user':user})

login_api = Blueprint('resources.validate', __name__)

api = Api(login_api)
api.add_resource(Login, '/api/v1/validate', endpoint='login')
api.add_resource(Register, '/api/v1/register', endpoint='register')

