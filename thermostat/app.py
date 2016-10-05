import random
import uuid
from flask import Flask
from flask_restful import Resource, Api
import requests

app = Flask(__name__)
api = Api(app)

HUB_HOST = 'localhost'
HUB_PORT = 3001
random_port = random.randrange(8001, 8099)

thermostat_information = {
    "name": "",
    "target": 70,
    "current": random.randrange(65, 75),
    "history": [],
}

class Thermostat(Resource):
    def get(self, target=None, current=None, history=None):
        current_temperature = random.randrange(65, 75)
        thermostat_information['current'] = current_temperature
        return thermostat_information

    def post(self, name=None, target=None):
        return ['post thermostat info']

api.add_resource(Thermostat, '/')


my_info = {
    "ip": "localhost",
    "port": random_port,
    "id": str(uuid.uuid1()),
}

if __name__ == '__main__':
    # register this instance with the hub
    # requests.post("http://" + HUB_HOST + ':' + str(HUB_PORT), json=my_info)

    # need to check if we can actually bind to this port
    app.run(host='localhost', port=random_port)
