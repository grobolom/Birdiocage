from flask_pymongo import PyMongo
from flask import Flask, jsonify, redirect, url_for
from flask_restful import Resource, Api

app = Flask(__name__)
app.config["MONGO_DBNAME"] = "birdcage_hub"
mongo = PyMongo(app, config_prefix='MONGO')
api = Api(app)

class Thermostat(Resource):
    def get(self, id=None):
        data = []

        if id:
            info = mongo.db.thermostat.find_one({"_id": id})
            if info:
                return jsonify({"status": "ok", "data": info})
            else:
                return {"response": "no thermostat registered under id {}".format(id)}

        cursor = mongo.db.thermostat.find(None, {"_id":1,"name": 1})
        for thermostat in cursor:
            data.append(thermostat)
        return jsonify({"response": data})

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
api.add_resource(Temperature, '/temperature')
api.add_resource(Registry, '/register')

if __name__ == '__main__':
      app.run(host='localhost', port=3001)
