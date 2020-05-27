"""
    connected-home.__main__
    ~~~~~~~~~~~~~~

    by Data-Centric Design Lab
    :license: MIT
"""

from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json

from .entities.thing import Thing
from .entities.light import Light
from .entities.switch import Switch

app = Flask(__name__)
CORS(app)


def findThingById(thing_id):
    for thing in things:
        print(thing.id)
        if thing.id == thing_id:
            return thing

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/things', methods = ['GET'])
def list():
    return json.dumps([thing.__dict__ for thing in things])

@app.route('/things/<path:thing_id>', methods = ['GET'])
def read(thing_id):
    global things
    return json.dumps(findThingById(thing_id).__dict__)

@app.route('/things/<path:thing_id>/controls/<path:control_id>', methods = ['GET'])
def control(thing_id, control_id):
    print('control ' + control_id + ' of ' + thing_id)
    response = {}
    response["result"] = getattr(findThingById(thing_id), control_id)()
    return json.dumps(response)

@app.route('/things', methods = ['POST'])
def create():
    global things
    things.append(Thing(request.json["name"]))
    return 'Added thing!'

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))
    emit('json', json, broadcast=True)

def send_ws_message(json):
    emit('json', json, broadcast=True)

light1 = Light('Test light')
switch1 = Switch('Test switch')
switch1.switch_on()

things = [light1, switch1]

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=80)
    

