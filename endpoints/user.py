from flask import Blueprint, jsonify
from flask_restful import reqparse, Resource, Api, marshal_with, marshal, fields
from models.user import *
from peewee import *
import datetime as dt

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
           if User.get(User.UserName == args['username']).Password == args['password'] and User.get(User.UserName == args['username']).Active == 'Active':
               return jsonify({'statusCode':200,'username':args['username']})
           elif  User.get(User.UserName == args['username']).Password == args['password'] and User.get(User.UserName == args['username']).Active == 'Deactivated':
               print('Entered')
               return jsonify({'statusCode': 202})
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

    def post(self):
        args = self.reqparse.parse_args()
        User.create(**args)
        return jsonify({'statusCode': 200, 'result': 'success'})

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
            individual_instance['Charge'] = sensor.ChargePerHour
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
                                  , SensorDetails.Region == args['region'])
        q.execute()
        return jsonify({'statusCode': 200})

class EditSensor(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorType', required=True, help='sensorType is required', location=['form', 'json'])
        self.reqparse.add_argument('region', required=True, help='region is required', location=['form', 'json'])
        self.reqparse.add_argument('charges', required=True, help='charges is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        print(args)
        q = SensorDetails.update(ChargePerHour=args['charges']).where(SensorDetails.Region == args['region']
            , SensorDetails.SensorType == args['sensorType']
                                  )
        q.execute()
        return jsonify({'statusCode': 200})

class GetUserInfo(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

    def post(self):
        result = []
        count_instances = 0
        query = User.select()
        userInfo = query.execute()

        for userdetail in userInfo:
            individual_instance = {}
            individual_instance['UserName'] = userdetail.UserName
            individual_instance['Emailid'] = userdetail.EmailId
            individual_instance['isActive'] = userdetail.Active
            q = Sensor.select().where(Sensor.UserName == userdetail.UserName).count()
            print(q)
            individual_instance['SensorCount'] = q
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'userInfo':result})

class ActivateUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        query = User.select(User.Active).where(User.UserName == args['username'])
        resultRec = query.execute()
        finalVal = ''
        for userdetail in resultRec:
            finalVal = userdetail.Active
        if(finalVal == 'Active'):
            return jsonify({'statusCode': 201})
        else:
            q = User.update(Active='Active').where(User.UserName == args['username'])
            q.execute()
            return jsonify({'statusCode': 200})

class DeactivateUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        query = User.select(User.Active).where(User.UserName == args['username'])
        resultRec = query.execute()
        finalVal = ''
        for userdetail in resultRec:
            finalVal = userdetail.Active
        if(finalVal == 'Deactivated'):
            return jsonify({'statusCode': 201})
        else:
            q = User.update(Active='Deactivated').where(User.UserName == args['username'])
            q.execute()
            return jsonify({'statusCode': 200})

class DeleteUser(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        q = User.delete().where(User.UserName == args['username'])
        q.execute()
        q = Sensor.delete().where(Sensor.UserName == args['username'])
        q.execute()
        q = SensorCluster.delete().where(SensorCluster.UserName == args['username'])
        q.execute()
        return jsonify({'statusCode': 200})

class GetSensorDetailsMonitor(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        count_instances = 0
        query = Sensor.select().where(Sensor.UserName == args['username'] , Sensor.Status != 'terminated')
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorHubName'] = sensor.SensorHubName
            individual_instance['SensorId'] = sensor.SensorId
            individual_instance['SensorType'] = sensor.SensorType
            individual_instance['Region'] = sensor.Region
            individual_instance['Status'] = sensor.Status
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'sensorInfo':result})

class GetSensorDetailsMonitorCluster(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        count_instances = 0
        query = SensorCluster.select().where(SensorCluster.UserName == args['username'] , SensorCluster.Status != 'terminated')
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorHubName'] = sensor.SensorHubName
            individual_instance['Status'] = sensor.Status
            q = Sensor.select().where(Sensor.UserName == args['username'] , Sensor.SensorHubName == sensor.SensorHubName , Sensor.Status != 'terminated').count()
            individual_instance['Count'] = q
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'clusterInfo':result})

class GetSensorDetailsMonitorClusterAdmin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        count_instances = 0
        query = SensorCluster.select().where(SensorCluster.Status != 'terminated')
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorHubName'] = sensor.SensorHubName
            individual_instance['Status'] = sensor.Status
            q = Sensor.select().where(Sensor.SensorHubName == sensor.SensorHubName , Sensor.Status != 'terminated').count()
            individual_instance['Count'] = q
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'clusterInfo':result})

class GetSensorDetailsMonitorAdmin(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        result = []
        count_instances = 0
        query = Sensor.select().where(Sensor.Status != 'terminated')
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorHubName'] = sensor.SensorHubName
            individual_instance['SensorId'] = sensor.SensorId
            individual_instance['SensorType'] = sensor.SensorType
            individual_instance['Status'] = sensor.Status
            individual_instance['UserName'] = sensor.UserName
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)

        return jsonify({'statusCode': 200,'sensorInfo':result})


login_api = Blueprint('resources.validate', __name__)

api = Api(login_api)
api.add_resource(Login, '/api/v1/validate', endpoint='login')
api.add_resource(Register, '/api/v1/register', endpoint='register')
api.add_resource(AdminLogin, '/api/v1/adminValidate', endpoint='adminlogin')
api.add_resource(GetSensorInfo, '/api/v1/getSensorDetails', endpoint='getsensorinfo')
api.add_resource(DeleteSensor, '/api/v1/deleteSensor', endpoint='deletesensor')
api.add_resource(EditSensor, '/api/v1/editSensor', endpoint='editsensor')
api.add_resource(GetUserInfo, '/api/v1/getUserDetails', endpoint='getuserdetails')
api.add_resource(ActivateUser, '/api/v1/activate', endpoint='activateuser')
api.add_resource(DeactivateUser, '/api/v1/deactivate', endpoint='deactivateuser')
api.add_resource(DeleteUser, '/api/v1/deleteuser', endpoint='deleteuser')
api.add_resource(GetSensorDetailsMonitor, '/api/v1/getSensorDetailsMonitor', endpoint='getsensordetailsmonitor')
api.add_resource(GetSensorDetailsMonitorAdmin, '/api/v1/getSensorDetailsMonitorAdmin', endpoint='getsensordetailsmonitoradmin')
api.add_resource(GetSensorDetailsMonitorCluster, '/api/v1/getSensorDetailsMonitorCluster', endpoint='getsensordetailsmonitorcluster')
api.add_resource(GetSensorDetailsMonitorClusterAdmin, '/api/v1/getSensorDetailsMonitorClusterAdmin', endpoint='getsensordetailsmonitorclusteradmin')



