from flask import Blueprint, jsonify
from flask_restful import reqparse, Resource, Api, marshal_with, marshal, fields
from models.user import *
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

class AdminLogin(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])
        self.reqparse.add_argument('password', required=True, help='password is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        try:
           if Admin.get(Admin.UserName == args['username']).Password == args['password']:
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

class GetSensorInfo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def post(self):
        result = []
        count_instances = 0
        query = SensorDetails.select()
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorType'] = sensor.SensorType
            individual_instance['Region'] = sensor.Region
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'sensorInfo':result})

class DeleteSensor(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorType', required=True, help='sensorType is required', location=['form', 'json'])
        self.reqparse.add_argument('region', required=True, help='region is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        q = SensorDetails.delete().where(SensorDetails.SensorType == args['sensorType']
                                  and SensorDetails.Region == args['region'])
        q.execute()
        return jsonify({'statusCode': 200})


login_api = Blueprint('resources.validate', __name__)

api = Api(login_api)
api.add_resource(Login, '/api/v1/validate', endpoint='login')
api.add_resource(Register, '/api/v1/register', endpoint='register')
api.add_resource(AdminLogin, '/api/v1/adminValidate', endpoint='adminlogin')
api.add_resource(GetSensorInfo, '/api/v1/getSensorDetails', endpoint='getsensorinfo')
api.add_resource(DeleteSensor, '/api/v1/deleteSensor', endpoint='deletesensor')

