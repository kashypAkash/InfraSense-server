import boto3, json

from flask import Flask, Blueprint, render_template, request
from flask_cors import CORS
from flask_restful import reqparse
from endpoints.validate import login_api
from models.models import initialize

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(login_api)

app.secret_key = '2#$$#SFGA#$@%FSG%#??|{KJHJK{KNKJK?KKJ\mnkjj'
parser = reqparse.RequestParser()
parser.add_argument('username',required=True,
                    help='Name cannot be blank!', location=['form','json'])
parser.add_argument('password',required=True,
                    help='password cannot be blank!',location=['form','json'])
parser.add_argument('email',required=True,
                    help='email cannot be blank!',location=['form','json'])

@app.route('/')
def index():
    return render_template('index.html')

'''@app.route('/')
def hello_world():
    ec2 = boto3.resource('ec2')
    instance = ec2.Instance('i-07d5d55d9facb5790')
    print(instance.start())
    return "hello world"'''


@app.route('/userValidate',methods=['POST'])
def user_validate():
    print(request.json)
    return json.dumps(dict({'id':'i\'m coming from previous state','statusCode':200}))


@app.route('/adminValidate',methods=['POST'])
def admin_validate():
    print(request.json)
    if request.json['username'] == 'a':
        return json.dumps(dict({'id':'hello world','statusCode':200}))
    return json.dumps(dict({'statusCode':400}))


if __name__ == '__main__':
    initialize()
    app.run(debug=True,port=5000)