import socketio
import json
from urllib.parse import urlencode


#************************************************************************
#* Private Functions
#***********************************************************************/

def normalize_consumer(consumer):

    if consumer is None:
        return {'or': []}

    elif isinstance(consumer, str):

        return {'or': [consumer]}

    elif isinstance(consumer, list):

        return {'or': consumer}

    else:
        return consumer

def normalize_array(producer):

    if producer is None:
        return []

    elif not isinstance(producer, list):
        return [producer]

    else:
        return producer


#************************************************************************
#* Public Functions
#***********************************************************************/


class connect():


    def __init__(self, uri=None, username=None, password=None, operator=None, environment=None, consume=None, produce=None, channels=None):

        print(f'connecting to server at {uri}')

        query = json.dumps({
            'username': username,
            'password': password,
            'operator': operator,
            'environment': environment,
            'consume': normalize_consumer(consume),
            'produce': normalize_array(produce),
            'channels': normalize_array(channels),
        })

        self.socket = socketio.Client()

        self.listeners = []


        @self.socket.on('connect')
        def on_connect():
            print('Successfully connected.')


        class task():
            def __init__(self, socket, payload):
                self.payload = payload
                self.data = payload['data']
                self.topics = payload['topics']
                self.socket = socket


            def produce(self, topic=None, data=None):

                if topic is None:
                    raise Exception('Producers must include a topic.')
                if data is None:
                    raise Exception("'data', must not be 'None'.")

                production_payload = {
                    'topic': topic,
                    'stream_id': self.payload['stream_id'],
                    'channel': self.payload['channel'],
                    'data': data,
                }

                print(f'Producing Topic: {topic}')

                self.socket.emit('production', production_payload)




        @self.socket.on('consumption')
        def consumption(payload):

            for listener in self.listeners:

                listener(task(self.socket, payload))


        @self.socket.on('error')
        def on_error(error):
            print(error)

        @self.socket.on('info')
        def on_info(info):
            print(info)

        self.socket.connect(f'{uri}?init={query}')

        self.socket.sleep(3)



    def consume(self, func):

        self.listeners.append(func)


    def produce(self, topic=None, channel=None, data=None):


        if topic is None:
            raise Exception('Producers must include a topic.')
        if channel is None:
            raise Exception('Raw production must include a channel.')
        if data is None:
            raise Exception("'data', must not be 'None'.")

        print(f'Producing Topic: {topic}')

        self.socket.emit('production', {
            'topic': topic,
            'channel': channel,
            'data': data,
        })







#************************************************************************
#* Public Export
#***********************************************************************/