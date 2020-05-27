from enum import Enum
from typing import Dict, Tuple

from flask_restful import Api

from automd.automd import AutoMD
from automd.encoder import AutoMDObjEncoder
from automd.endpoints.openmd_html import AutoMDHTML
from automd.endpoints.openmd_spec import OpenAPISpecJSON, OpenAPISpecYAML
from automd.http_verbs import HTTPVerb
from automd.keys import AutoMDKeys


class AutoMDSpecRoute(Enum):
    html = "html"
    json = "json"
    yml = "yaml"
    yaml = "yaml"


class AutoMDApp:
    def __init__(
            self,
            app_api: Api,
            title: str,
            app_version: str = "0.0.1",
            openapi_version: str = "3.0.0",
            info: Dict = None,
            default_tag: str = None,
            path_override: str = None,
            spec_routes: Tuple = (AutoMDSpecRoute.html, AutoMDSpecRoute.yaml, AutoMDSpecRoute.json),
            always_document: bool = False,
            documented_verbs: Tuple = (HTTPVerb.get, HTTPVerb.post, HTTPVerb.put, HTTPVerb.delete, HTTPVerb.patch)
    ):
        """
        Configures OpenAPI documentation generator for the FlaskRESTful application.
        Also extends flask.json.JSONEncoder in the application config key "RESTFUL_JSON".

        :param app_api: FlaskRESTful API app to instantiate the documentation for.
        :param title: Application title
        :param app_version: Application version
        :param openapi_version: OpenAPI spec version presented.
        :param info: Detailed information about the application.
                        See https://github.com/OAI/OpenAPI-Specification/blob/master/versions/3.0.2.md#openapi-object
        :param default_tag: Tag to apply to endpoints if not specified in their decorator.
        :param path_override: Replaces the base path of the documentation routes.
                              Defaults to "/automd" (note leading, not trailing '/')
                              # TODO better path handling that string
        :param spec_routes: List containing routes to register, defaults to all.  List is made of
                            AutoMDSpecRoute enums
        :param always_document: Apply basic documentation to all endpoints, even if undecorated.
        :param documented_verbs: Tuple of what HTTP Verbs to document.  Defaults to GET, POST, PUT, DELETE, PATCH
        """
        self.app_api: Api = app_api
        self.app_api.app.config[AutoMDKeys.config.value] = self
        self.app_api.app.config["RESTFUL_JSON"] = {"cls": AutoMDObjEncoder}

        self.auto_md: AutoMD = AutoMD(title=title,
                                      app_version=app_version,
                                      openapi_version=openapi_version,
                                      info=info,
                                      default_tag=default_tag,
                                      always_document=always_document,
                                      documented_verbs=documented_verbs)

        endpoint_prefix: str = "automd"
        url: str = f"/{endpoint_prefix}" if path_override is None else path_override

        spec_routes = () if spec_routes is None else spec_routes
        if AutoMDSpecRoute.json in spec_routes:
            app_api.add_resource(OpenAPISpecJSON, f"{url}/spec/json", endpoint=f"OpenAPISpecJSON_{endpoint_prefix}")
        if AutoMDSpecRoute.yaml in spec_routes or AutoMDSpecRoute.yml in spec_routes:
            app_api.add_resource(OpenAPISpecYAML, f"{url}/spec/yaml", endpoint=f"OpenAPISpecYAML_{endpoint_prefix}")
        if AutoMDSpecRoute.html in spec_routes:
            app_api.add_resource(AutoMDHTML, f"{url}/html", endpoint=f"OpenAPIHTML_{endpoint_prefix}")
