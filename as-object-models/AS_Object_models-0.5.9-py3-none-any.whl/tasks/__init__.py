from .. client_utils import FirestoreClient
import json

DOWNLOAD = 'download'
UPDATE_ITEM = 'updateItem'
PROCESS_UPLOAD = 'processUpload'

def send_task(queue_name, handler, payload):
    '''
    Expectation is that the payload will be a dict... we'll dump that to json, then encode
    '''
    clt = FirestoreClient.getInstance()
    task = {
        'app_engine_http_request': {
            'http_method': 'POST',
            'relative_uri': handler
        }
    }

    converted_payload = json.dumps(payload).encode()
    task['app_engine_http_request']['body'] = converted_payload

    path = clt.task_queues.get(queue_name,None)
    if path is None:
        raise Exception("Invalid Queue Name")

    response = clt.tasksClient.create_task(path, task)
    print('Created task {}'.format(response.name))
    return response