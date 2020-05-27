from typing import Dict

from apispec import APISpec
from flask import current_app
from flask_restful import Resource

from automd.decorators import automd
from automd.automd import AutoMD
from automd.keys import AutoMDKeys


class OpenAPISpecJSON(Resource):
    @automd(summary="OpenAPI JSON Documentation Endpoint",
            description="Returns the OpenAPI Spec in JSON format",
            tags=["AutoMD"])
    def get(self) -> Dict:
        auto_app: AutoMD = current_app.config[AutoMDKeys.config.value].auto_md

        automd_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: Dict = automd_spec.to_dict()

        return ret


class OpenAPISpecYAML(Resource):
    @automd(summary="OpenAPI Yaml Documentation Endpoint",
            description="Returns the OpenAPI Spec in Yaml format",
            tags=["AutoMD"])
    def get(self) -> str:
        auto_app: AutoMD = current_app.config[AutoMDKeys.config.value].auto_md

        automd_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: str = automd_spec.to_yaml()

        return ret
