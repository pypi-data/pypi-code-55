"""

This function allows you to transfer from your wallet to other identities. If you enable notify by email, you will receive an email every time the url is called with your APP Key.

URL :
https://greydotapi.me/?par2=[Amount]&par1=[Send to Identity]&k=[APP Key]&do=[FID]

[Amount] is the amount to send
[Send to Identity] the identity that will recieve the digits
[APP Key] Your APP Key
[FID]The function ID for Wallet transfer is 2

Example url :
https://greydotapi.me/?par2=1&par1=25911000000&k=abcdefghijklmnopqrst&do=2

Example reply :

    {
        "query": {
            "query_result": {
                "status": "Success",
                "function": "Wallet transfer",
                "amount": "1",
                "to": "25911000000"
            },
            "query_status": "DONE",
            "query_code": "D0002"
        }
    }

"""
from sms import GREYDOT_APP_KEY, API_URL, parse_xml_response
import requests
import urllib.parse

FID = 2
SAMPLE = """
<?xml version="1.0" encoding="utf-8" ?>
<query>
    <query_result>
        <status>Success</status>
        <function>Wallet transfer</function>
        <amount>1</amount>
        <to>25911000000</to>
    </query_result>
    <query_status>DONE</query_status>
    <query_code>D0002</query_code>
</query>
"""


def send_money(Amount=0.0, To=""):
    params = {
        "par1": To,
        "par2": Amount,
        "k": GREYDOT_APP_KEY,
        "do": FID,
    }
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(API_URL, params=encoded_params)
    print(response.url)
    return parse_xml_response(response.text)
