from flask import Flask
from flask_cors import CORS
from endpoints.user import login_api
from endpoints.aws import aws_api
from models.user import initialize

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.register_blueprint(login_api)
app.register_blueprint(aws_api)

DEBUG = True
PORT = 5000

app.secret_key = '2#$$#SFGA#$@%FSG%#??|{KJHJK{KNKJK?KKJ\mnkjj'

if __name__ == '__main__':
    initialize()
    app.run(debug=DEBUG, port=PORT)