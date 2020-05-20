"""
This function allows you to sign up new customers directly. If you enable notify by email, you will also receive an email every time the url is called with your APP Key.

URL :
https://greydotapi.me/?k=[APP Key]&do=[FID] &par1=[First Name]&par2=[Last Name]&par3=[Email] &par4=[Mobile]&par5=[ReferralCode]&par6=[GroupCode] &par7=[WelcomeEmail]&par8=[WelcomeSMS]

**APP Key** : Your APP Key
**FID]The function ID for Signup is 19
**First Name** : First name of the customer being signed up _required_
**Last Name** : Last name of the customer being signed up _optional_
**Email** : Email of the customer being signed up _optional_
**Mobile** : Mobile number of the customer being signed up _required_
**ReferralCode** : Your ReferralCode _optional_
**GroupCode** : Your GroupCode if you have one _optional_
**WelcomeEmail** : If set to 1 customer being signed up will get a email with his account info_optional_
**WelcomeSMS** : If set to 1 customer being signed up will get an sms with his account info _optional_

If par7 and par8 is set to 0 or not specified the customer being signed up will get no welcome correspondence.

Example 1 url :
https://greydotapi.me/?k=abcdefghijklmnopqrst&do=19&par1=Joe&par2=Black&par3=joe@email.me&par4=0898887744&par5=1234

Example reply :

    {
        "query": {
            "query_result": {
                "status": "Success",
                "function": "SignUp",
                "signup_status": "Registered",
                "identity": "0123456789",
                "password": "9876543210",
                "appkey": "abcdefghijklmnopqrst"
            },
            "query_status": "DONE",
            "query_code": "D0017"
        }
    }

"""
from sms import GREYDOT_APP_KEY, API_URL, parse_xml_response
import requests
import urllib.parse
from collections import defaultdict

FID = 19
SAMPLE = """

<?xml version="1.0" encoding="utf-8" ?>
<query>
    <query_result>
        <status>Success</status>
        <function>SignUp</function>
        <signup_status>Registered</signup_status>
        <identity>0123456789</identity>
        <password>9876543210</password>
        <appkey>abcdefghijklmnopqrst</appkey>
    </query_result>
    <query_status>DONE</query_status>
    <query_code>D0017</query_code>
</query>
"""


def register(
    fname: str,
    mobile: str,
    lname=None,
    email=None,
    refcode="",
    groupcode=None,
    welcomemail=0,
    welcomesms=1,
):
    """
    Params::

    **fname** : First name of the customer being signed up _required_
    **lname** : Last name of the customer being signed up _optional_
    **email** : Email of the customer being signed up _optional_
    **mobile** : Mobile number of the customer being signed up _required_
    **refcode** : Your ReferralCode _optional_
    **groupcode** : Your GroupCode if you have one _optional_
    **welcomemail** : If set to 1 customer being signed up will get a email with his account info _optional_
    **welcomesms** : If set to 1 customer being signed up will get an sms with his account info _optional_
    """
    params = defaultdict()
    params["do"] = FID
    params["k"] = GREYDOT_APP_KEY
    params["par1"] = fname
    params["par4"] = mobile
    params["par8"] = welcomesms
    if lname:
        params["par2"] = lname
    if email:
        params["par3"] = email
        params["par7"] = 1
    if refcode:
        params["par5"] = refcode
    if groupcode:
        params["par6"] = groupcode
    if not email:
        params["par7"] = welcomemail
    encoded_params = urllib.parse.urlencode(params)
    response = requests.get(API_URL, params=encoded_params)
    print(response.url)
    return parse_xml_response(response.text)
