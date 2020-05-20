"""
Use the API to send an sms to a number. If you enable notify by email, you will receive an email every time the url is called with your APP Key.

URL :
https://greydotapi.me/?par1=[Number-to-SMS]&par2=[url-encoded-text-message]&k=[APP-Key]&do=[FID]

[**Number to SMS**] Number that will receive the sms message or list of numbers each separated by an e

[**url encoded text message**] Text to be sent to number in url encoded form

[**APP Key**] Your APP Key

[**FID**] The function ID for Send sms is 11



Bulk Example url :
https://greydotapi.me/?par1=0820000000e0820000001e0820000002&par2=Test+sms%2C+Hallo+world.&k=abcdefghijklmnopqrst&do=11

Example url :
https://greydotapi.me/?par1=0820000000&par2=Test+sms%2C+Hallo+world.&k=abcdefghijklmnopqrst&do=11

Example reply :

    {
        "query": {
            "query_result": {
                "status": [
                    "Success",
                    "Send_SMS"
                ],
                "to": "27110000000",
                "sms_id": "000"
            },
            "query_status": "DONE",
            "query_code": "D0011"
        }
    }

"""
import requests
import os
import xmltodict
from json import dumps, loads
import urllib.parse

API_URL = "https://greydotapi.me/"
FID = 11
if os.environ.get("GREYDOT_APP_KEY") is not None:
    GREYDOT_APP_KEY = os.environ.get("GREYDOT_APP_KEY")
else:
    GREYDOT_APP_KEY = "fe43abd74579155d4e05"
    # GREYDOT_APP_KEY = "GREYDOT_APP_KEY"
    # raise ValueError("GREYDOT_APP_KEY environment variable is not set.")

SAMPLE = """
<?xml version="1.0" encoding="utf-8" ?>

<query>

<query_result>

<status>Success</status>

<status>Send_SMS</status>

<to>27110000000</to>

<sms_id>000</sms_id>

</query_result>

<query_status>DONE</query_status>

<query_code>D0011</query_code>

</query>

"""


def parse_xml_response(response):
    """
    **Args**::

    - `response`: String of raw xml response returned

    **Returns**::

    >
    {
        'result_status':"Success",
        'to':'27110000000',
        'sms_id':'0001',
        'query_status':'DONE',
        'query_code':'D0011'
    }


    """
    # print(response)
    try:
        doc = dumps(xmltodict.parse(response[response.find("<?xml"):]))
        print(doc)
        return loads(doc)
    except Exception:
        return {
            "result_status": "result_status",
            "to": "to",
            "sms_id": "sms_id",
            "query_status": "query_status",
            "query_code": "query_code",
        }


def send_sms(recipients=[], message="Test Message"):
    """
    **Args**::

    - `recipients`: Number that will receive the sms message or list of numbers

    - `message`: Text to be sent to number

    **Returns**::

    >
    {
        'result_status':"Success",
        'to':'27110000000',
        'sms_id':'0001',
        'query_status':'DONE',
        'query_code':'D0011'
    }



    """
    if len(recipients) > 1:
        par1 = "e".join(recipients)
    else:
        par1 = recipients[0]

    params = {
        "par1": par1,
        "par2": message,
        "k": GREYDOT_APP_KEY,
        "do": FID,
    }
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(API_URL, params=encoded_params)
    print(response.url)
    return parse_xml_response(response.text)
