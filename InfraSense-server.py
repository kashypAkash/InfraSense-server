import boto3, json

from flask import Flask, Blueprint, render_template, request
from flask_cors import CORS
from endpoints.user import login_api
from endpoints.aws import aws_api
from models.user import initialize

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(login_api)
app.register_blueprint(aws_api)

app.secret_key = '2#$$#SFGA#$@%FSG%#??|{KJHJK{KNKJK?KKJ\mnkjj'


@app.route('/')
def index():
    return render_template('index.html')


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