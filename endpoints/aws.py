import boto3
import botocore.exceptions

from flask import Blueprint, jsonify
from flask_restful import Resource, Api, reqparse

# Creating the Connection
ec2 = boto3.resource('ec2')


class Create(Resource):

    ''' This is resource is for creating or launching New Instances'''
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('imageid', required=True, help='image_id required'
                               , location=['form', 'json'])
    def post(self):
        args = self.reqparse.parse_args()
        try:
            instances = [instance.id for instance in ec2.create_instances(
                ImageId=args['imageid'], MinCount=1, MaxCount=5, InstanceType='t2.micro')]
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


aws_api = Blueprint('endpoints.aws', __name__)
api = Api(aws_api)
api.add_resource(Create, '/api/v1/create', endpoint='createinstance')
api.add_resource(Active, '/api/v1/active', endpoint='activeinstances')
api.add_resource(Health, '/api/v1/health', endpoint='instancehealth')
api.add_resource(Start, '/api/v1/start', endpoint='start')