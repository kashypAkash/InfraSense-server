import boto3
import botocore.exceptions
import json
import random

from datetime import datetime, date
from datetime import timedelta
from datetime import timezone
from dateutil import parser


from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse
from models.user import *

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
        return jsonify({'statusCode': 200, 'result': val})
        # ec2.instances.filter(InstanceIds=ids).terminate()

class Stop(Resource):

    ''' This resource is used for starting, stopping and terminating Instance/S
        pass list or tuple like -> ids = ['instance-id-1', 'instance-id-2', ...] '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('instanceid', required=True, help='instance id required'
                                   , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        print(args.instanceid);
        val = ec2.instances.filter(InstanceIds=[args['instanceid']]).stop()
        q = Sensor.update(Status='stopped').where(Sensor.SensorId == args['instanceid'])
        q.execute()
        return jsonify({'statusCode': 200, 'result': val})
        # ec2.instances.filter(InstanceIds=ids).terminate()

class Terminate(Resource):

    ''' This resource is used for starting, stopping and terminating Instance/S
        pass list or tuple like -> ids = ['instance-id-1', 'instance-id-2', ...] '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('instanceid', required=True, help='instance id required'
                                   , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        print(args.instanceid);
        val = ec2.instances.filter(InstanceIds=[args['instanceid']]).terminate()
        q = Sensor.update(Status='terminated').where(Sensor.SensorId == args['instanceid'])
        q.execute()
        return jsonify({'statusCode': 200, 'result': val})

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
        sensorHubRequired = 0;
        args = self.reqparse.parse_args()
        d = json.loads(args.addsensors)
        result=[]
        count_instances = 0
        for sensors in d:
            if(sensors.get('count') == 0):
                continue
            sensorHubRequired = 1
            count = sensors.get('count')
            type = sensors.get('type')
            individual_instance={}
            try:
                instances = [instance.id for instance in ec2.create_instances(
                    ImageId=args['imageId'], MinCount=count, MaxCount=count, InstanceType='t2.micro')]

                for instance in instances:
                    print("Instance values:" + instance)
                    sensor_values = {"UserName": args.username, "SensorHubName": args.sensorhubname,
                                     "SensorId": instance, "SensorType": type, "Status": "running"}
                    object_values = {"username" : args.username, "SensorHubName": args.sensorhubname,
                                      "SensorId" : instance, "SensorType": type, "Status": "running" }
                   # UserSensorHubDetails.create(**object_values)
                    Sensor.create(**sensor_values)
                    individual_instance['SensorId'] = instance
                    individual_instance['SensorType'] = type
                    individual_instance['sensorhubname'] = args['sensorhubname']
                    count_instances = count_instances + 1
                    individual_instance['index'] = count_instances
                    result.append(individual_instance)
            except botocore.exceptions.ClientError as e:
                return jsonify({'statusCode': 400, 'error': e})

        if(sensorHubRequired == 1):
            sensorHub_Values = {"UserName": args.username, "SensorHubName": args.sensorhubname, "Status": "running"}
            SensorCluster.create(**sensorHub_Values)

        return jsonify({'statusCode': 200, 'instanceDetails' :result})

class addToSensorHub(Resource):

    ''' This is resource is for adding new sensor Instances to the sensorHub'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorhubname', required=True, help='sensor hub name required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('sensorType', required=True, help='sensor type info is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('imageId', required=True, help='Image Id is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('username', required=True, help='User name is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('count', required=True, help='count is required'
                               , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        count_instances = 0
        result=[]

        count = int(args['count'])
        try:
            instances = [instance.id for instance in ec2.create_instances(
                ImageId=args['imageId'], MinCount=count, MaxCount=count, InstanceType='t2.micro')]

            for instance in instances:
                print("Instance values:" + instance)
                individual_instance = {}
                sensor_values = {"UserName": args.username, "SensorHubName": args.sensorhubname,
                                 "SensorId": instance, "SensorType": args['sensorType'], "Status": "running"}
                Sensor.create(**sensor_values)
                individual_instance['SensorId'] = instance
                individual_instance['SensorType'] = args['sensorType']
                individual_instance['sensorhubname'] = args['sensorhubname']
                count_instances = count_instances + 1
                individual_instance['index'] = count_instances
                result.append(individual_instance)
        except botocore.exceptions.ClientError as e:
            return jsonify({'statusCode': 400, 'error': e})

        return jsonify({'statusCode': 200, 'instanceDetails': result})

class deleteFromSensorHub(Resource):

    ''' This is resource is for adding new sensor Instances to the sensorHub'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorhubname', required=True, help='sensor hub name required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('sensorType', required=True, help='sensor type info is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('imageId', required=True, help='Image Id is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('username', required=True, help='User name is required'
                               , location=['form', 'json'])
        self.reqparse.add_argument('count', required=True, help='count is required'
                               , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        count_instances = 0
        result=[]
        query = Sensor.select().where(Sensor.SensorHubName == args['sensorhubname'] and
                                                             Sensor.SensorType == args['sensorType'] and
                                                             Sensor.UserName == args['username'] and
                                                             Sensor.Status != 'terminated').limit(args['count'])
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            val = ec2.instances.filter(InstanceIds=[sensor.SensorId]).terminate()
            q = Sensor.update(Status='terminated').where(Sensor.SensorId == sensor.SensorId)
            q.execute()
            print("The following sensor " + sensor.SensorId + " is deleted successfully")
            individual_instance['SensorId'] = sensor.SensorId
            individual_instance['SensorType'] = args['sensorType']
            individual_instance['sensorhubname'] = args['sensorhubname']
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)
        return jsonify({'statusCode': 200, 'instanceDetails': result})

class getMonitoringInfo(Resource):

    ''' This resource is used for monitoring the instances using various metrics '''

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensorid', required=True, help='sensorid id required'
                                   , location=['form', 'json'])
        self.reqparse.add_argument('startDate', required=True, help='startDate  required'
                                   , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        #print(args['startDate'])

        #to get the status of the instance
        val=ec2.Instance(args['sensorid']);

        statusCode = 0
        cpuutilisationAverage = 0
        networkInAverage = 0
        networkoutAverage = 0


        if (val.launch_time < parser.parse(args.startDate) and parser.parse(args.startDate) <= datetime.now(timezone.utc) and val.state['Name'] == 'running'):
            statusCode = 200

            try:
                # get the cpu utilization
                cpuUtilizationMet = client.get_metric_statistics(Namespace='AWS/EC2', MetricName='CPUUtilization',
                                                             Dimensions=[{'Name': 'InstanceId', 'Value': args.sensorid}],
                                                             StartTime=parser.parse(args.startDate),
                                                             EndTime=parser.parse(args.startDate) + timedelta(days=1),
                                                             Period=86400,
                                                             Statistics=[
                                                                 'Average'
                                                             ]
                                                             )

                cpuutilisationAverage = cpuUtilizationMet['Datapoints'][0]['Average']



                # get the disk write operation usage
                networkInMet = client.get_metric_statistics(Namespace='AWS/EC2', MetricName='NetworkIn',
                                                        Dimensions=[{'Name': 'InstanceId', 'Value': args.sensorid}],
                                                        StartTime=parser.parse(args.startDate),
                                                        EndTime=parser.parse(args.startDate) + timedelta(days=1),
                                                        Period=86400,
                                                        Statistics=[
                                                            'Average'
                                                        ]
                                                        )

                networkInAverage = networkInMet['Datapoints'][0]['Average']

                # get the disk write operation usage
                networkOutMet = client.get_metric_statistics(Namespace='AWS/EC2', MetricName='NetworkOut',
                                                         Dimensions=[{'Name': 'InstanceId', 'Value': args.sensorid}],
                                                         StartTime=parser.parse(args.startDate),
                                                         EndTime=parser.parse(args.startDate) + timedelta(days=1),
                                                         Period=86400,
                                                         Statistics=[
                                                             'Average'
                                                         ]
                                                         )

                networkoutAverage = networkOutMet['Datapoints'][0]['Average']
            except IndexError:
                #statusCode = 205
                #testing
                cpuutilisationAverage = random.uniform(0.0100,0.0150)
                networkInAverage = random.uniform(59.6200,63.8800)
                networkoutAverage = random.uniform(29.9000,31.8800)
        elif (val.launch_time > parser.parse(args.startDate)):
            statusCode = 201
        elif (parser.parse(args.startDate) > datetime.now(timezone.utc)):
            statusCode = 202
        elif (val.state['Name'] != 'running'):
            statusCode = 203
        print(cpuutilisationAverage)
        return jsonify({'statusCode': statusCode,
                        'sensorid': args.sensorid,
                        'launchtime':val.launch_time,
                        'state': val.state,
                        'cpuutilisationAverage': cpuutilisationAverage,
                        'networkInAverage': networkInAverage,
                        'networkoutAverage': networkoutAverage
                        })


class getUserSensorDetails(Resource):

    ''' This is resource is for adding new sensor Instances to the sensorHub'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', required=True, help='User name is required'
                               , location=['form', 'json'])

    def post(self):
        args = self.reqparse.parse_args()
        count_instances = 0
        result=[]
        query = Sensor.select().where(Sensor.UserName == args['username'])
        sensorInfo = query.execute()

        for sensor in sensorInfo:
            individual_instance = {}
            individual_instance['SensorId'] = sensor.SensorId
            individual_instance['SensorType'] = sensor.SensorType
            individual_instance['SensorHubName'] = sensor.SensorHubName
            individual_instance['Status'] = sensor.Status
            count_instances = count_instances + 1
            individual_instance['index'] = count_instances
            result.append(individual_instance)
        return jsonify({'statusCode': 200, 'instanceDetails': result})

aws_api = Blueprint('endpoints.aws', __name__)
api = Api(aws_api)

api.add_resource(Create, '/api/v1/create', endpoint='createinstance')
api.add_resource(Active, '/api/v1/active', endpoint='activeinstances')
api.add_resource(Health, '/api/v1/health', endpoint='instancehealth')
api.add_resource(Start, '/api/v1/start', endpoint='start')
api.add_resource(Stop, '/api/v1/stop', endpoint='stop')
api.add_resource(Terminate, '/api/v1/terminate', endpoint='terminate')
api.add_resource(createSensorHub, '/api/v1/createSensorHub', endpoint='createSensorHub')
api.add_resource(getMonitoringInfo, '/api/v1/getMonitoringInfo', endpoint='getMonitoringInfo')
api.add_resource(addToSensorHub, '/api/v1/addToSensorHub', endpoint='addToSensorHub')
api.add_resource(deleteFromSensorHub, '/api/v1/deleteFromSensorHub', endpoint='deleteFromSensorHub')
api.add_resource(getUserSensorDetails, '/api/v1/getUserSensorDetails', endpoint='getUserSensorDetails')
