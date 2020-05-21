import io
import requests
import json
from threading import Timer
from datetime import datetime

buffer = []
buffer_size = 5
timeout=10

def setBufferLength(len):
    global buffer_size
    buffer_size = len


def setTimerTime(time):
    global timeout
    timeout = time






def hit_the_api(buffer):
    # will complete it soon
    print(buffer_size,timeout)
    print('inside hit api')
    API_ENDPOINT = "http://127.0.0.1:9000/"
    data = json.dumps(buffer)
    print(buffer,"   ",type(buffer)," ",type(data))
    r = requests.post(url=API_ENDPOINT, data=data)
    buffer.clear()
    t = Timer(timeout, hit_the_api,[buffer])
    t.start()
    
    


def sendlog(message):
    now = datetime.now() 
    date_time = now.strftime("%m/%d/%Y , %H:%M:%S")
    message=date_time+" "+message
    if (len(buffer) == buffer_size):
        hit_the_api(buffer)
        buffer.append(message)
    else:
        buffer.append(message)



