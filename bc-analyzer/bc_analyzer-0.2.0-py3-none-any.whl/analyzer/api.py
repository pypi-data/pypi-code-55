import requests
from . import globals


def get_queued_analysis(id):
    response = requests.get(
        globals.get_full_url("queuedanalysis/%s" % (id)), headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_queued_analysis_index(path: str, ended=None, public=None):
    relative_url = "queuedanalysis?path=%s" % (path)
    if ended:
        relative_url += "&ended=1"
    if public:
        relative_url += "&public=1"
    response = requests.get(globals.get_full_url(relative_url), headers=globals.get_headers(),)
    response.raise_for_status()
    return response.json()


def queued_analysis_mark_started(id):
    response = requests.put(
        globals.get_full_url("queuedanalysis/%s/mark_started" % (id)),
        headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def queued_analysis_mark_ended(id):
    response = requests.put(
        globals.get_full_url("queuedanalysis/%s/mark_ended" % (id)), headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def get_dataset(id):
    response = requests.get(
        globals.get_full_url("datasets/%s" % (id)), headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def dataset_attach_data(id, data, extension):
    response = requests.put(
        globals.get_full_url("datasets/%s/attach_data" % (id)),
        json={"data": data, "extension": extension},
        headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def dataset_update_state(id, fields):
    response = requests.put(
        globals.get_full_url("datasets/%s/update_state" % (id)),
        json=fields,
        headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()


def dataset_abort_upload(id):
    response = requests.put(
        globals.get_full_url("datasets/%s/abort_upload" % (id)), headers=globals.get_headers(),
    )
    response.raise_for_status()
    return response.json()
