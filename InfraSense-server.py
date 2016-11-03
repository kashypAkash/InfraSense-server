import boto3, json

from flask import Flask,request,render_template, session
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.secret_key = '2#$$#SFGA#$@%FSG%#??|{KJHJK{KNKJK?KKJ\mnkjj'

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


@app.route('/addUser', methods=['POST'])
def add_user():
    print(request.json)
    return json.dumps(dict({'id':'user added', 'statusCode':200}))


if __name__ == '__main__':
    app.run(debug=True,port=5000)