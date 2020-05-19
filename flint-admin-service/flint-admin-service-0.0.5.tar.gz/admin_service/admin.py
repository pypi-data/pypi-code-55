from flask import Flask, request, jsonify
from admin_service.functions import get_token
import os

application = Flask(__name__)
flint_authentication = ""


class App:

    def __init__(self):
        self.authentication = ""

    def register_authentication(self, authentication):
        global flint_authentication
        flint_authentication = authentication

    @staticmethod
    @application.route('/', methods=['POST'])
    def user():
        missing_args = []
        data = request.get_json()
        user_info = data.get("data", None)
        user_id = data.get("user", None)
        if user_info is None:
            missing_args.append("data")
        if user_id is None:
            missing_args.append("user")
        if len(missing_args) > 0:
            message = "Flint Admin Service API Missing params: {}".format(', '.join(missing_args))
            response = {
                "message": message,
                "status": "failure"
            }
        else:
            result = flint_authentication(**user_info)
            if result:
                token = get_token(user_id)
                response = {
                    "user": user_id,
                    "token": token,
                    "message": "",
                    "status": "success"
                }
            else:
                message = "User {} is not authenticated".format(user_id)
                response = {
                    "user": user_id,
                    "message": message,
                    "status": "failure"
                }
        return jsonify(response)

    @staticmethod
    def start():
        debug = os.getenv("DEBUG")
        if debug == "true":
            application.config["DEBUG"] = True
            application.config["ENV"] = "development"
            application.run(host='0.0.0.0', port='8080')
        else:
            application.run(host='0.0.0.0', port='8080')


def create_app():
    return App()
