# Birdiocage

# Hub API

```
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
```

# Thermostat API

```
localhost:8001-8099

GET /thermostat
GET /thermostat/:fields
    fields = current, target, history
POST /info
    name = String
    target = Int
```

# Installation and Running

```
# install requirements
source venv/bin/activate
pip install -r requirements.txt

# build mongo container
docker-compose build
docker-compose start

# run applications
python hub/app.py &
python thermostat/app.py &
python thermostat/app.py &
python thermostat/app.py &
python thermostat/app.py &
python thermostat/app.py &
```

In the future, we would run the hub through WSGI and spin up the smaller
apps probably through docker containers
