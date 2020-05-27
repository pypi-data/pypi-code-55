from typing import Dict

from apispec import APISpec
from flask import current_app, Response as FlaskResponse
from flask_restful import Resource

from automd.decorators import automd
from automd.automd import AutoMD
from automd.keys import AutoMDKeys
from automd.templates.openapi import generate_template_from_dict


class AutoMDHTML(Resource):
    @automd(summary="OpenAPI HTML Documentation Endpoint",
            description="Returns the OpenAPI HTML",
            tags=["AutoMD"])
    def get(self) -> str:
        auto_app: AutoMD = current_app.config[AutoMDKeys.config.value].auto_md

        automd_spec: APISpec = auto_app.application_to_apispec(current_app)

        ret: Dict = automd_spec.to_dict()

        return FlaskResponse(generate_template_from_dict(ret), mimetype="text/html")
