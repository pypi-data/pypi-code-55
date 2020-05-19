"""
Module to use the websocket API with an appliance.
"""
import asyncio
import copy
import inspect
import json
import logging
import sys
import string
import traceback

import websockets
import requests
import os
import random
from pathlib import Path


LOGGER = logging.getLogger(__name__)

# If the logging level is set to DEBUG then websockets logs very verbosely,
# including a hex dump of every message being sent. Setting the websockets
# logger at INFO level specifically prevents this spam.
logging.getLogger("websockets.protocol").setLevel(logging.INFO)
#AUTHEN_URL = "https://api-dev2.vais.vn/authen"
#ANALYTIC_URL = "https://api-dev2.vais.vn/analytic"
AUTHEN_URL = "https://vaisapis.vais.vn/authen"
ANALYTIC_URL = "https://vaisapis.vais.vn/analytic"
API_KEY = ""

def log_error(msg):
    print(msg)

def verify_output(resp):
    if resp.status_code >= 400:
        try:
            output = resp.json()
            if "code" in output and output["code"] != 200:
                log_error(output["message"])
                return True, output["message"]
        except json.decoder.JSONDecodeError:
            return True, resp.text
    return False, None

def get_authen_file():
    homedir = str(Path.home())

    vaisasr_dir = os.path.join(homedir, ".vaisasr")
    if not os.path.exists(vaisasr_dir):
        os.makedirs(vaisasr_dir)
    return os.path.join(vaisasr_dir, "credentials.json")

def get_plugin_result(audio_id, plugin_code="all"):
    parts = plugin_code.split(".")
    code = parts[0]

    get_url = ANALYTIC_URL + '/v1/audios/' + audio_id + '/plugin-data'
    # params = '?' + '&'.join(('plugin_code=' + code))
    params = '?plugin_code=' + code
    r = requests.get(get_url + params, headers=get_header())
    assert r.status_code == 200
    output = r.json()
    for p in parts:
        if isinstance(output, dict) and p in output:
            output = output[p]
        else:
            raise Exception("Failed to parse data extractor:", plugin_code, ":", p, "does not in output")
            return output
    return output


def get_text(audio_id):
    get_url = ANALYTIC_URL + '/v1/texts?audio_id=' + audio_id
    # params = '?' + '&'.join(('plugin_code=' + code))
    r = requests.get(get_url, headers=get_header())
    err, msg = verify_output(r)
    if err:
        return err, msg

    output = r.json()

    text = output["data"]
    while output["has_more"]:
        next_page = output["next_page"]
        if next_page == -1:
            break
        r = requests.get(get_url + "&page=" + str(next_page), headers=get_header())
        err, msg = verify_output(r)
        if err:
            return err, msg
        output = r.json()
        text += r.json()["data"]
    return text


def login(email, password):
    r = requests.post(AUTHEN_URL + "/api/v1/auth/login", json={"email": email, "password": password})
    err, msg = verify_output(r)
    if err:
        return err, msg

    credential_file = get_authen_file()

    output_dict = r.json()
    open(credential_file, "w").write(json.dumps(output_dict))

    apis = list_apis()
    if apis:
        api = apis[0]
        output_dict["api"] = api
        open(credential_file, "w").write(json.dumps(output_dict))
    return False, None


def get_header():
    if not API_KEY:
        credential_file = get_authen_file()
        assert os.path.exists(credential_file), "User unauthorized. Run `vais login` command to login"
        credential = json.loads(open(credential_file, "r").read())
        assert "access_token" in credential, "Access token not found. Run `vais login` command to login"

        if "api" in credential:
            return {"Api-key": credential["api"]["api_key"]}
        else:
            return {"token": credential["access_token"]}
    else:
        return {"Api-key": API_KEY}

def get_upload_url(file_name, audiosource_id):
    r = requests.post(ANALYTIC_URL + "/v1/digitalization/upload-audio",
            json={
                "file_name": file_name,
                "audiosource_id": audiosource_id
                },
            headers=get_header())
    err, msg = verify_output(r)
    if err:
        return err, msg
    return False, r.json()

def create_audio(name, audiosource_id, bucket, key):
    r_audio = requests.post(ANALYTIC_URL + "/v1/audios",
            json={
                "name": name,
                "audiosource_id": audiosource_id,
                "bucket": bucket,
                "key": key
                },
            headers=get_header())
    verify_output(r_audio)
    r_execute = requests.post(ANALYTIC_URL + "/v1/audios/execute-plan",
            json={
                "audio_id": r_audio.json()["id"]
                },
            headers=get_header())
    verify_output(r_execute)
    return r_audio.json()


def upload_file(file_path, audiosource_id=None):
    if not audiosource_id:
        source = list_source()
        assert len(source) > 0, "You don't have any audio source configured, please access the web page and setup one."
        LOGGER.debug("Source id is not specified, use the default one")
        audiosource_id = source[0]["id"]
    LOGGER.debug("Uploading file to source " + audiosource_id)

    file_name, ext = os.path.splitext(os.path.basename(file_path))
    file_name += "_".join(random.choices(string.digits, k=4)) + ext

    err, upload_info = get_upload_url(file_name, audiosource_id)
    if err:
        return err, upload_info
    host = upload_info["postEndpoint"]
    signature = upload_info["signature"]

    audio_fd = open(file_path, "rb")
    files =  {'file': audio_fd}
    LOGGER.info("Uploading file")
    r = requests.post(host, data=signature, files=files, timeout=600)
    err, msg = verify_output(r)
    if err:
        return err, msg
    LOGGER.info("Upload complete")

    audio = create_audio(file_name, audiosource_id, signature["bucket"], signature["key"])
    LOGGER.info("Queued audio with id: " + audio["id"])
    return False, audio

async def monitor_status(audio_id):
    WS_ANALYTIC_URL = ANALYTIC_URL.replace("https", "wss").replace("http", "ws")
    URL = WS_ANALYTIC_URL + "/v1/monitor/ws/audio-status?audio_id=" + audio_id
    async with websockets.connect(URL) as websocket:
        while True:
            info = await websocket.recv()
            info = json.loads(info)
            if info["status"] in [4, 5]:
                LOGGER.info("Completed")
                return info["message"]
            LOGGER.info(info)

def list_source():
    r = requests.get(ANALYTIC_URL + "/v1/audio-sources",
            headers=get_header())
    assert r.status_code == 200, r.text
    return r.json()["data"]

def list_apis():
    r = requests.get(ANALYTIC_URL + "/api/v1/apikeys",
            headers=get_header())
    assert r.status_code == 200, r.text
    return r.json()["data"]
