# Birdiocage

# Hub API

localhost:3001

GET /thermostats
GET /thermostats/:id
POST /thermostats
    temperature = Int
POST /thermostats
    id = Int
    temperature = Int
GET /temperature

POST /register
    id = UID
    ip = IP
    port = Int

# Thermostat API

localhost:8001-8099

GET /thermostat
GET /thermostat/:fields
    fields = current, target, history
POST /info
    name = String
    target = Int
