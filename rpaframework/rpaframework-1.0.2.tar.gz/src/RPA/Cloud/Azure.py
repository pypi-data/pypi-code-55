import json
import requests
from RPA.core.utils import required_env


class Azure:
    """Library for interacting with Azure services

    Requires environment variable `AZURE_SUBSCRIPTION_KEY`
    to use.

    https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest
    """

    COGNITIVE_API = "api.cognitive.microsoft.com"
    STORAGE_API = "api.storage.microsoft.com"

    def __init__(self, region="northeurope"):
        self.region = region

    def _set_request_headers(self, content_type=None):
        subscription_key = required_env("AZURE_SUBSCRIPTION_KEY")
        headers = {
            "Ocp-Apim-Subscription-Key": subscription_key,
        }
        if content_type and content_type == "binary":
            headers["Content-Type"] = "application/octet-stream"
        return headers

    def _azure_post(self, url, params=None, filepath=None, jsondata=None):
        request_parameters = {}
        if filepath:
            request_parameters["headers"] = self._set_request_headers("binary")
            with open(filepath, "rb") as f:
                filedata = f.read()
            request_parameters["data"] = filedata
        if jsondata:
            request_parameters["headers"] = self._set_request_headers()
            request_parameters["json"] = jsondata
        if params:
            request_parameters["params"] = params
        response = requests.post(url, **request_parameters)
        return response

    def vision_analyze(
        self, image_file: str, json_file: str = None, region: str = None
    ):
        if region is None:
            region = self.region
        analyze_url = f"https://{region}.{self.COGNITIVE_API}/vision/v3.0/analyze"
        params = {"visualFeatures": "Categories,Description,Color"}
        response = self._azure_post(analyze_url, params=params, filepath=image_file)
        if json_file and response:
            with open(json_file, "w") as f:
                json.dump(response.json(), f)
        return response.json()

    def sentiment_analyze(self, documents, json_file=None, region: str = None):
        if region is None:
            region = self.region
        analyze_url = (
            f"https://{region}.{self.COGNITIVE_API}/text/analytics/v3.0/sentiment"
        )
        response = self._azure_post(analyze_url, jsondata=documents)
        if json_file and response:
            with open(json_file, "w") as f:
                json.dump(response.json(), f)
        return response.json()
