from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Thermostat(Resource):
    def get(self):
        return ['get thermostats']
    def post(self):
        return ['post thermostats']

class Temperature(Resource):
    def get(self):
        return ['get average temp']

class Registry(Resource):
    def post(self):
        return ['post new thermostat']

api.add_resource(Thermostat, '/thermostats')
api.add_resource(Temperature, '/temperature')
api.add_resource(Registry, '/register')

if __name__ == '__main__':
      app.run(host='localhost', port=3001)
