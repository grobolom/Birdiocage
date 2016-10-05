import json
from bson import ObjectId
from flask_pymongo import PyMongo
from flask import Flask, jsonify, redirect, url_for, request
from flask_restful import Resource, Api
import requests

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

def update_thermostats(query, target):
    cursor = mongo.db.thermostat.find(query)
    for thermostat in cursor:
        ip = str(thermostat.get('ip'))
        port = str(thermostat.get('port'))
        url = "http://" + ip + ":" + port + "/"
        requests.post(url, json={"target":target})

def update_thermostat_data(query):
    cursor = mongo.db.thermostat.find(query)
    data = []
    for thermostat in cursor:
        ip = str(thermostat.get('ip'))
        port = str(thermostat.get('port'))
        url = "http://" + ip + ":" + port + "/"

        try:
            r = requests.get(url)
        except ConnectionError as e:
            mongo.db.thermostat.delete_one({"id": thermostat.get("id")})
            continue

        if r:
            result = r.json()
            thermostat["current"] = result.get("current")
            thermostat["target"] = result.get("target")
            thermostat["name"] = result.get("name")

            mongo.db.thermostat.replace_one({"id": thermostat.get("id")}, thermostat)

class Thermostat(Resource):
    def get(self, id=None):
        data = []

        if id:
            update_thermostat_data({"_id": ObjectId(id)})
            info = mongo.db.thermostat.find_one({"_id": ObjectId(id)})
            if info:
                return JSONEncoder().encode({"status": "ok", "data": info})
            else:
                return {"response": "no thermostat registered under id {}".format(id)}

        update_thermostat_data({})
        cursor = mongo.db.thermostat.find(None, {"_id":1,"name": 1})
        for thermostat in cursor:
            data.append(thermostat)
        return JSONEncoder().encode({"response": data})

    def post(self, id=None):
        data = request.get_json()

        query = {}
        if id:
            query = {"_id": ObjectId(id)}

        update_thermostats(query, data.get('target'))

        return redirect(url_for("thermostats"))

class Temperature(Resource):
    def get(self):
        result = mongo.db.thermostat.aggregate([{
            "$group": {
                "_id": None,
                "avg_temp": { "$avg": "$current" }
            }
        }])
        for r in result:
            return JSONEncoder().encode({"status": "ok", "average_temperature": r["avg_temp"]})

class Registry(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"response": "ERROR"}

        mongo.db.thermostat.insert(data)

        return {"status": "ok"}

api.add_resource(Thermostat, '/thermostats', endpoint="thermostats")
api.add_resource(Thermostat, '/thermostats/<id>', endpoint="id")
api.add_resource(Temperature, '/temperature')
api.add_resource(Registry, '/register')

if __name__ == '__main__':
      app.run(host='localhost', port=3001)
