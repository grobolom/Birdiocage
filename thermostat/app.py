import random
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Thermostat(Resource):
    def get(self, target=None, current=None, history=None):
        return ['get thermostat info']
    def post(self, name=None, target=None):
        return ['post thermostat info']

api.add_resource(Thermostat, '/')

random_port = random.randrange(8001, 8099)

if __name__ == '__main__':
      app.run(host='localhost', port=random_port)
