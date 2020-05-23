"""
This function allows you to query your Airtime balance. If you enable notify by email, you will receive an email every time the url is called with your APP Key.

URL :
https://greydotapi.me/?k=[APP Key]&do=[FID]

[**APP Key**] Your APP Key

[**FID**]The function ID for Airtime balance is 5


Example url :
https://greydotapi.me/?k=abcdefghijklmnopqrst&do=5

Example reply :

    {
        "query": {
            "query_result": {
                "status": "Success",
                "function": "Airtime balance",
                "amount": "20.00"
            },
            "query_status": "DONE",
            "query_code": "D0005"
        }
    }

"""

SAMPLE = """
    <?xml version="1.0" encoding="utf-8" ?>

    <query>

    <query_result>

    <status>Success</status>

    <function>Airtime balance</function>

    <amount>20.00</amount>

    </query_result>

    <query_status>DONE</query_status>

    <query_code>D0005</query_code>

    </query>
"""
