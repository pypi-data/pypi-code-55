#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import paho.mqtt.client
from paho.mqtt.client import topic_matches_sub
import re
import time
import json
from .shc_client import *
from pprint import pprint


class xComforMqtt:

    def __init__(self, config):
        self._prefix = config['mqtt']['prefix']
        if self._prefix and not self._prefix.endswith('/'):
            self._prefix = self._prefix + '/'
        self._zones = {}
        self._devices = {}
        self._common_zone_ids = []
        self._subs = {}

        logging.info('SHC host: %s', config['shc']['host'])

        self._shc = SHC_Client(**config['shc'])

        self._mqtt = paho.mqtt.client.Client()

        if config['mqtt'].get('username', None):
            self._mqtt.username_pw_set(config['mqtt']['username'],
                                       config['mqtt'].get('password', None))

        if config['mqtt'].get('cafile', None):
            self._mqtt.tls_set(config['mqtt']['cafile'],
                               config['mqtt'].get('certfile', None),
                               config['mqtt'].get('keyfile', None))

        self._mqtt.on_connect = self._on_mqtt_connect
        self._mqtt.on_disconnect = self._on_mqtt_disconnect
        self._mqtt.on_message = self._on_mqtt_message

        self._mqtt.message_callback_add(self._prefix + '+/+/value/set', self._value_set)
        self._mqtt.message_callback_add(self._prefix + '+/+/state/set', self._value_set)
        self._mqtt.message_callback_add(self._prefix + '+/+/+/get', self._get)

        logging.info('MQTT broker host: %s, port: %d, use tls: %s',
                     config['mqtt']['host'],
                     config['mqtt']['port'],
                     bool(config['mqtt'].get('cafile', None)))

        self._mqtt.connect_async(config['mqtt']['host'], config['mqtt']['port'], keepalive=10)
        self._mqtt.loop_start()

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        logging.info('Connected to MQTT broker with code %s', rc)

        lut = {paho.mqtt.client.CONNACK_REFUSED_PROTOCOL_VERSION: 'incorrect protocol version',
               paho.mqtt.client.CONNACK_REFUSED_IDENTIFIER_REJECTED: 'invalid client identifier',
               paho.mqtt.client.CONNACK_REFUSED_SERVER_UNAVAILABLE: 'server unavailable',
               paho.mqtt.client.CONNACK_REFUSED_BAD_USERNAME_PASSWORD: 'bad username or password',
               paho.mqtt.client.CONNACK_REFUSED_NOT_AUTHORIZED: 'not authorised'}

        if rc != paho.mqtt.client.CONNACK_ACCEPTED:
            logging.error('Connection refused from reason: %s', lut.get(rc, 'unknown code'))

        if rc == paho.mqtt.client.CONNACK_ACCEPTED:
            for topic in ('+/+/value/set', '+/+/state/set', '+/+/+/get'):
                topic = self._prefix + topic
                logging.debug('Subscribe: %s', topic)
                client.subscribe(topic)

    def _on_mqtt_disconnect(self, client, userdata, rc):
        logging.info('Disconnect from MQTT broker with code %s', rc)

    def _on_mqtt_message(self, client, userdata, message):
        logging.debug('mqtt_on_message %s %s', message.topic, message.payload)

    def _value_set(self, client, userdata, message):
        logging.debug('_value_set %s %s', message.topic, message.payload)
        device = self._subs.get(message.topic[:-4], None)
        if not device:
            self._mqtt.publish(message.topic[:-10] + '/error', 'unknown device')
            return

        try:
            value = json.loads(message.payload.decode())
        except Exception as e:
            logging.warning(e)

        if device['type'] == 'LightActuator' or device['type'] == 'SwitchActuator':
            if value not in device['operations']:
                set_value = bool(value)
                value = 'on' if set_value else 'off'

        elif device['type'] == 'DimActuator':
            if isinstance(value, bool):
                self._mqtt.publish(message.topic[:-10] + '/error', 'device unsupported set %s use int' % value)
                return
            else:
                value = int(value)
                if value < 0:
                    value = 0
                elif value > 100:
                    value = 100
            set_value = value
        else:
            self._mqtt.publish(message.topic[:-10] + '/error', 'device unsupported set value')
            return

        resp = self._shc.control_device(device['zone_ids'][0], device['id'], value)
        if resp['status'] == 'ok':
            if value == 'toggle':
                return

            device['value'] = set_value

            payload = json.dumps(device['value'])
            for topic in device['topics']:
                self._mqtt.publish(topic, payload)

    def _get(self, client, userdata, message):
        logging.debug('_value_get %s %s', message.topic, message.payload)
        device_topic = message.topic[:-4]
        device = self._subs.get(device_topic, None)
        if not device:
            self._mqtt.publish(device_topic + '/error', 'unknown device or value')
            return

        self._mqtt.publish(device_topic, json.dumps(device['value']))

    def start(self):
        self._zones_load()

        while True:
            self._update()
            time.sleep(1)

    def _update(self):
        for zone_id in self._common_zone_ids:
            for udevice in self._shc.get_devices(zone_id):
                device = self._devices[udevice['id']]

                if udevice['value'] == '?':
                    udevice['value'] = None
                elif device['type'] == 'DimActuator':
                    udevice['value'] = int(udevice['value'])
                elif udevice['type'] == 'LightActuator' or udevice['type'] == 'SwitchActuator':
                    udevice['value'] = True if udevice['value'] == 'ON' else False
                else:
                    udevice['value'] = float(udevice['value'])

                if udevice['value'] != device['value']:
                    device['value'] = udevice['value']
                    payload = json.dumps(device['value'])
                    for topic in device['topics']:
                        self._mqtt.publish(topic, payload)

    def _zones_load(self):
        self._devices = {}
        self._zones = {}

        for zone in self._shc.get_zones():
            zone_devices = self._shc.get_devices(zone['zoneId'])
            zone['devices'] = {}
            zone['zoneName'] = zone['zoneName'].strip()
            self._zones[zone['zoneId']] = zone

            for device in zone_devices:
                if not device['id'] in self._devices:
                    device['zone_ids'] = []
                    device['topics'] = []
                    self._devices[device['id']] = device

                device = self._devices[device['id']]
                device['zone_ids'].append(zone['zoneId'])
                zone['devices'][device['id']] = device
                device['name'] = device['name'].strip()

                device_topic = self._prefix + zone['zoneName'] + '/' + device['name']
                device_topic = re.sub(r'[\s+#-]+', '-', device_topic).strip()

                if device['type'] == 'LightActuator' or device['type'] == 'SwitchActuator':
                    device_topic += '/state'
                elif device['type'] == 'DimActuator':
                    device_topic += '/value'
                elif device['type'] == 'TemperatureSensor':
                    device_topic = re.sub(r'-?\(temperature\)', '', device_topic) + '/temperature'
                elif device['type'] == 'HumiditySensor':
                    device_topic = re.sub(r'-?\(humidity\)', '', device_topic) + '/humidity'
                elif device['type'] == 'ValveSensor':
                    device_topic = re.sub(r'-?\(position\)', '', device_topic) + '/position'
                else:
                    device_topic += '/value'

                device['topics'].append(device_topic)
                device['value'] = None

                self._subs[device_topic] = device

        # calculation of common zones
        udevices = {}

        for zone_id in self._zones:
            lz = len(self._zones[zone_id]['devices'])

            for device_id in self._zones[zone_id]['devices']:
                udevice = udevices.get(device_id, None)

                if udevice:
                    if udevice[1] > lz:
                        continue

                udevices[device_id] = [zone_id, lz]

        common_zone_ids = []
        for _, udevice in udevices.items():
            if not udevice[0] in common_zone_ids:
                common_zone_ids.append(udevice[0])

        self._common_zone_ids = common_zone_ids
