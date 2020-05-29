from venmo_api import Client
import requests
# token = Client.get_access_token(username="angelmamalionly@yahoo.com", password="x:V)jVc2aND}au", device_id="80642349-75K3-4F18-04Y7-4MG22V099XU5")
token = "72e9abfd940152ae583c40e17b2c13539253169a1b8a33db26c8c4e202f2f1c3"
client = Client(token)
# print(client.user.search_for_users("Niloo Tehrani")[0])

# transactions = client.user.get_user_transactions(user=client.user.get_my_profile())
#
# for t in transactions:
#     print(t)
print(client.user.get_my_profile())
# method = 'POST'
# url = 'https://api.venmo.com/v1/oauth/access_token'
# header_params = {'device-id': '80642349-75K3-4F18-04Y7-4MG22V099XU5', 'Content-Type': 'application/json', 'Host': 'api.venmo_api.com'}
# params = None
#
# body = {'phone_email_or_username': 'emmaameli134@gmail.com', 'client_id': '1', 'password': 'RamzeGhavi9*'}
#
# response = requests.request(
#     method=method, url=url, headers=header_params, params=params, json=body)
#
# print(response.json())
