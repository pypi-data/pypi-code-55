#!/usr/bin/python
import socketio
import requests
import json

_BASE_URL = "https://config.aspecto.io"
# _BASE_URL = "http://localhost:8080"


def get_config_http(token):
    config = requests.get(_BASE_URL + "/config/" + token)
    return json.loads(config.content.decode("utf-8"))


def get_config(token, callback):
    sio = socketio.Client()

    @sio.on("config")
    def on_config(config):
        callback(config)

    @sio.on("connect")
    def on_connect():
        sio.emit("get-config")

    @sio.event
    def connect_error(e):
        print("Error", e)
        pass

    @sio.event
    def disconnect():
        print("Disconnect")
        pass

    sio.connect(_BASE_URL + "?token=" + token)
    sio.wait()
