import boto3
import botocore.exceptions
import json
from datetime import datetime


from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from models.user import UserSensorHubDetails
from flask_cors import cross_origin
# Creating the Connection
ec2 = boto3.resource('ec2')
client = boto3.client('cloudwatch')


class Create(Resource):

    ''' This is resource is for creating or launching New Instances'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('imageId', required=True, help='image_id required'
                               , location=['form', 'json'])
    def post(self):
        args = self.reqparse.parse_args()
        try:
            instances = [instance.id for instance in ec2.create_instances(
                ImageId=args['imageId'], MinCount=1, MaxCount=5, InstanceType='t2.micro')]
            return jsonify({'statusCode':200,'instanceids':instances})
        except botocore.exceptions.ClientError as e:
            return jsonify({'statusCode':400,'error':e.message})


class Start(Resource):

    ''' This resource is used for starting, stopping and terminating Instance/S
        pass list or tuple like -> ids = ['instance-id-1', 'instance-id-2', ...] '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('instanceid', required=True, help='instance id required'
                                   , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        val = ec2.instances.filter(InstanceIds=[args['instanceid']]).start()
        print(val)
        # ec2.instances.filter(InstanceIds=ids).terminate()

class Active(Resource):

    ''' This resource is for Checking What Instances Are Running'''

    def get(self):
        instances = ec2.instances.filter(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
        '''for instance in instances:
            print(instance.id, instance.instance_type) '''
        return instances


class Health(Resource):

    '''This resource is used for Checking Health Status Of Instances'''

    def get(self):
        for status in ec2.meta.client.describe_instance_status()['InstanceStatuses']:
            print(status)


class createSensorHub(Resource):

    '''This resource is used for Checking Health Status Of Instances'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorhubname', required=True, help='sensor hub name required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('addsensors', required=True, help='add sensor info is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('imageId', required=True, help='Image Id is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('username', required=True, help='User name is required'
                               , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        d = json.loads(args.addsensors)
        result=[]
        for sensors in d:
            if(sensors.get('count') == 0):
                continue
            count = sensors.get('count')
            type = sensors.get('type')
            individual_instance={}
            try:
                instances = [instance.id for instance in ec2.create_instances(
                    ImageId=args['imageId'], MinCount=count, MaxCount=count, InstanceType='t2.micro')]

                for instance in instances:
                    print("Instance values:" + instance)
                    object_values = {"username" : args.username, "SensorHubName": args.sensorhubname,
                                      "SensorId" : instance, "SensorType": type }
                    UserSensorHubDetails.create(**object_values)
                    individual_instance['SensorId'] = instance
                    individual_instance['SensorType'] = type
                    result.append(individual_instance)
            except botocore.exceptions.ClientError as e:
                return jsonify({'statusCode': 400, 'error': e})
        return jsonify({'statusCode': 200, 'instanceDetails' :result})


class getMonitoringInfo(Resource):

    ''' This resource is used for starting, stopping and terminating Instance/S
        pass list or tuple like -> ids = ['instance-id-1', 'instance-id-2', ...] '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorid', required=True, help='sensorid id required'
                                   , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()

        val=ec2.Instance(args['sensorid']);
        metricsVal = client.get_metric_statistics(Namespace='AWS/EC2',MetricName='CPUUtilization',
                                                  Dimensions=[{'Name': 'InstanceId', 'Value': args.sensorid}],
                                                  StartTime=datetime(2016, 11, 15),
                                                  EndTime=datetime(2016, 11, 17),
                                                  Period=86400,
                                                  Statistics=[
                                                      'Average'
                                                  ]
                                                  )
        print(type(metricsVal))
        print(metricsVal)

        return jsonify({'statusCode': 200, 'state': val.state,'metricsVal' : metricsVal})

aws_api = Blueprint('endpoints.aws', __name__)
api = Api(aws_api)
api.add_resource(Create, '/api/v1/create', endpoint='createinstance')
api.add_resource(Active, '/api/v1/active', endpoint='activeinstances')
api.add_resource(Health, '/api/v1/health', endpoint='instancehealth')
api.add_resource(Start, '/api/v1/start', endpoint='start')
api.add_resource(createSensorHub, '/api/v1/createSensorHub', endpoint='createSensorHub')
api.add_resource(getMonitoringInfo, '/api/v1/getMonitoringInfo', endpoint='getMonitoringInfo')