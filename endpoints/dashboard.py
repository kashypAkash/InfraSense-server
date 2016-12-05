from flask import Blueprint, jsonify
from flask_restful import reqparse, Resource, Api, marshal_with, marshal, fields
from models.user import User, Sensor, SensorCluster
from peewee import *

class Totalusers(Resource):

    '''def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])
        self.reqparse.add_argument('password', required=True, help='password is required', location=['form','json'])'''

    def get(self):
        return jsonify({'statusCode':200,'users': User.select().count()})

class Totalsensors(Resource):
    '''Get the total no of Sensor'''
    def get(self):
        return jsonify({'statusCode':200, 'sensors': Sensor.select().count()})

class Totalsensorsbyaccount(Resource):
    '''Get the total no of Sensor'''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        return jsonify({'statusCode':200, 'sensors': Sensor.select().where(Sensor.UserName == args['username']).count()})



class Totalclusters(Resource):

    '''Get the total no of cluster'''
    def get(self):
        return jsonify({'statusCode':200, 'cluster':SensorCluster.select().count()})

class Totalclusterbyaccount(Resource):
    '''Get the total no of Sensor'''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        return jsonify({'statusCode':200, 'cluster': SensorCluster.select().where(SensorCluster.UserName == args['username']).count()})



class Sensortypes(Resource):

    '''Get the total sensor types'''

    def get(self):
        return jsonify({'statusCode':200, 'sensorTypes':'4'})

class Sensorsbytype(Resource):

    def get(self):

        query = (Sensor
                 .select(Sensor.SensorType, fn.COUNT(Sensor.SensorId).alias('count'))
                 .group_by(Sensor.SensorType))
        count=[]
        types =[]
        for row in query.execute():
            count.append(row.count)
            types.append(row.SensorType)

        return jsonify({'statusCode':200, 'count':count, 'types':types})

class Sensorsbytypebyaccount(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        query = (Sensor
                 .select(Sensor.SensorType, fn.COUNT(Sensor.SensorId).alias('count'))
                 .where(Sensor.UserName==args['username']).group_by(Sensor.SensorType))
        count=[]
        types =[]
        for row in query.execute():
            count.append(row.count)
            types.append(row.SensorType)

        return jsonify({'statusCode':200, 'count':count, 'types':types})

class Sensorsperclusterbyaccount(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        query = (Sensor
                 .select(Sensor.SensorHubName, fn.COUNT(Sensor.SensorId).alias('count'))
                 .where(Sensor.UserName==args['username']).group_by(Sensor.SensorHubName))
        count=[]
        clusters =[]
        for row in query.execute():
            count.append(row.count)
            clusters.append(row.SensorHubName)

        return jsonify({'statusCode':200, 'count':count, 'clusters':clusters})


class Activesensors(Resource):

    def get(self):
        return jsonify({'statusCode':200, 'activesensors': Sensor.select().where(Sensor.Status == 'running').count()})

class Activesensorsbyaccount(Resource):
    '''Fetch the active sensor for a user'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        sensors = Sensor.select().where(Sensor.Status == 'running', Sensor.UserName==args['username'])
        result =[ {'status':sensor.Status,'sensorid':sensor.SensorId, 'clustername':sensor.SensorHubName,
                   'type':sensor.SensorType} for sensor in sensors]

        return jsonify({'statusCode':200, 'activesensors': sensors.count(),'result':result})


class Pendingsensors(Resource):

    def get(self):
        return jsonify({'statusCode':200, 'pendingsensors': Sensor.select().where(Sensor.Status == 'pending').count()})

class Pendingsensorsbyaccount(Resource):
    '''Fetch the pending sensor for a user'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        sensors = Sensor.select().where(Sensor.Status == 'stopped', Sensor.UserName==args['username'])
        result =[ {'status':sensor.Status,'sensorid':sensor.SensorId, 'clustername':sensor.SensorHubName,
                   'type':sensor.SensorType} for sensor in sensors]

        return jsonify({'statusCode':200, 'pendingsensors': sensors.count(),'result':result})



class Terminatedsensors(Resource):

    def get(self):
        return jsonify({'statusCode':200, 'terminatedsensors': Sensor.select().where(Sensor.Status == 'terminated').count()})


class Terminatedsensorsbyaccount(Resource):
    '''Fetch the pending sensor for a user'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='username is required', location=['form','json'])

    def post(self):
        args = self.reqparse.parse_args()
        sensors = Sensor.select().where(Sensor.Status == 'terminated', Sensor.UserName==args['username'])
        result =[ {'status':sensor.Status,'sensorid':sensor.SensorId, 'clustername':sensor.SensorHubName,
                   'type':sensor.SensorType} for sensor in sensors]

        return jsonify({'statusCode':200, 'terminatedsensors': sensors.count(),'result':result})



dashboard_api = Blueprint('resources.dashboard', __name__)

api = Api(dashboard_api)
# Common
api.add_resource(Sensortypes, '/api/v1/sensortypes', endpoint='sensortypes')

# Admin api
api.add_resource(Totalusers, '/api/v1/totalusers', endpoint='totalusers')
api.add_resource(Totalsensors, '/api/v1/totalsensors', endpoint='totalsensors')
api.add_resource(Totalclusters, '/api/v1/totalclusters', endpoint='totalclusters')
api.add_resource(Sensorsbytype, '/api/v1/typecount', endpoint='sensorsbytype')
api.add_resource(Activesensors, '/api/v1/activesensors', endpoint='activesensor')
api.add_resource(Pendingsensors, '/api/v1/pendingsensors', endpoint='pendingsensors')
api.add_resource(Terminatedsensors, '/api/v1/terminatedsensors', endpoint='terminatedsensors')

# User Api
api.add_resource(Totalsensorsbyaccount, '/api/v1/totalsensorsbyaccount', endpoint='totalsensorsbyaccount')
api.add_resource(Totalclusterbyaccount, '/api/v1/totalclusterbyaccount', endpoint='totalclusterbyaccount')
api.add_resource(Sensorsbytypebyaccount, '/api/v1/typecountbyaccount', endpoint='sensorsbytypebyaccount')
api.add_resource(Sensorsperclusterbyaccount, '/api/v1/sensorperclusterbyaccount', endpoint='sensorperclusterbyaccount')
api.add_resource(Activesensorsbyaccount, '/api/v1/activesensorsbyaccount', endpoint='activesensorbyaccount')
api.add_resource(Pendingsensorsbyaccount, '/api/v1/pendingsensorsbyaccount', endpoint='pendingsensorsbyaccount')
api.add_resource(Terminatedsensorsbyaccount, '/api/v1/terminatedsensorsbyaccount', endpoint='terminatedsensorsbyaccount')