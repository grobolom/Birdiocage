import random
import uuid
from flask import Flask, request
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
    def get(self, fields=None):
        current_temperature = random.randrange(65, 75)

        if fields == "current":
            return {"current" : current_temperature}
        elif fields == "target":
            return {"target": thermostat_information["target"]}
        elif fields == "history":
            return {"history": thermostat_information["history"]}

        thermostat_information['current'] = current_temperature
        return thermostat_information

    # if we were following better API design, this would likely be a
    # put endpoint for the various fields, but for simplicity we are
    # sticking with just the usual POST/GET until things get complex
    def post(self):
        data = request.get_json()

        if not data:
            return {"response": "ERROR"}

        name = data.get("name")
        if name:
            thermostat_information["name"] = name

        target = data.get("target")
        if target:
            thermostat_information["target"] = target

        # in a more complex API, we would probably do a redirect_for to
        # the correct endpoint
        return thermostat_information

api.add_resource(Thermostat,
    '/',
    '/<string:fields>',
    endpoint='thermostat')


my_info = {
    "ip": "localhost",
    "port": random_port,
    "id": str(uuid.uuid1()),
    "name": thermostat_information["name"],
    "current": thermostat_information["current"],
    "target": thermostat_information["target"],
}

if __name__ == '__main__':
    # register this instance with the hub
    requests.post("http://" + HUB_HOST + ':' + str(HUB_PORT) + "/register", json=my_info)

    # need to check if we can actually bind to this port
    app.run(host='localhost', port=random_port)
