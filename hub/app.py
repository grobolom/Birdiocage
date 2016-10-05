import json
from bson import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, jsonify, redirect, url_for, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "birdcage_hub"
mongo = PyMongo(app, config_prefix='MONGO')
api = Api(app)

# ripped from StackOverflow to properly encode BSON
class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

class Thermostat(Resource):
    def get(self, id=None):
        data = []

        if id:
            info = mongo.db.thermostat.find_one({"_id": ObjectId(id)})
            if info:
                return JSONEncoder().encode({"status": "ok", "data": info})
            else:
                return {"response": "no thermostat registered under id {}".format(id)}

        cursor = mongo.db.thermostat.find(None, {"_id":1,"name": 1})
        for thermostat in cursor:
            data.append(thermostat)
        return JSONEncoder().encode({"response": data})

    def post(self):
        return ['post thermostats']

class Temperature(Resource):
    def get(self):
        return ['get average temp']

class Registry(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"response": "ERROR"}

        mongo.db.thermostat.insert(data)

        return redirect(url_for("thermostats"))

api.add_resource(Thermostat, '/thermostats', endpoint="thermostats")
api.add_resource(Thermostat, '/thermostats/<id>', endpoint="id")
api.add_resource(Temperature, '/temperature')
api.add_resource(Registry, '/register')

if __name__ == '__main__':
      app.run(host='localhost', port=3001)
