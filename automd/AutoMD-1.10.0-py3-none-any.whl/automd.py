import mimetypes

from http.client import responses
from inspect import Signature
from typing import Dict, Union, List, Callable, Type, Tuple
from marshmallow import Schema, fields
from werkzeug.local import LocalProxy
from flask import url_for, Flask

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from werkzeug.routing import Rule, BuildError

from automd.decorators import automd
from automd.http_verbs import HTTPVerb
from automd.keys import AutoMDKeys
from automd.mixedfield import mixedfield_2properties
from automd.responses import ResponseObjectInterface
from automd.responses.responses import map_type_field_mapping, type_to_field


class AutoMD:
    def __init__(self,
                 title: str,
                 app_version: str = "1.0.0",
                 openapi_version: str = "3.0.0",
                 info: Dict = None,
                 default_tag: str = None,
                 always_document: bool = False,
                 documented_verbs: Tuple[HTTPVerb] = (HTTPVerb.get, HTTPVerb.post, HTTPVerb.put, HTTPVerb.delete)):
        """

        :param title: Application title
        :param app_version: Application version
        :param openapi_version: OpenAPI spec version presented.
        :param info: Detailed information about the application.
        :param default_tag: Tag to apply to endpoints if not specified in their decorator.
               Falls back to application title.
        :param always_document: Apply basic documentation to all endpoints, even if undecorated.
        :param documented_verbs: Tuple of what HTTP Verbs to document.  Defaults to GET, POST, PUT, DELETE, PATCH
        """
        self.always_document: bool = always_document
        self.default_tag: str = default_tag or title
        self.documented_verbs: Tuple[HTTPVerb] = documented_verbs
        self._ma_plugin: MarshmallowPlugin = MarshmallowPlugin()
        self.apispec_options: Dict = {
            "title": title,
            "app_version": app_version,
            "openapi_version": openapi_version,
            "info": {} if info is None else info,
            "plugins": [self._ma_plugin]
        }

    def start_spec(self) -> APISpec:
        """
        Returns a new APISpec object based off the parameters this class
        :return: new APISpec class
        """
        api_spec: APISpec = APISpec(self.apispec_options["title"],
                                    self.apispec_options["app_version"],
                                    self.apispec_options["openapi_version"],
                                    info=self.apispec_options["info"],
                                    plugins=self.apispec_options["plugins"])

        # register the Mixed Field handling function
        self._ma_plugin.converter.add_attribute_function(mixedfield_2properties)

        return api_spec

    @staticmethod
    def parse_parameter_schema(parameter_object: Union[Dict, Schema],
                               func_signature: Signature,
                               path_url: str,
                               http_verb: str) -> Dict[str, Dict[str, fields.Field]]:
        # No marhmallow parameters, infer from function signature
        if parameter_object is None:
            parameter_signature_dict = {}
            for name, param in func_signature.parameters.items():
                if name == "self":
                    continue

                field_args: Dict = {
                    "required": (param.default == Signature.empty)
                }

                if param.default != Signature.empty:
                    field_args["doc_default"] = param.default

                if param.default is None:
                    field_args["allow_none"] = param.default

                if map_type_field_mapping(param.annotation) in [fields.Raw, fields.Field]:
                    field_args["description"] = "parameter of unspecified type"

                field: fields.Field = type_to_field(param.annotation, **field_args)
                parameter_signature_dict[name] = field
            parameter_object = parameter_signature_dict

        # dump schema fields
        # TODO: this is probably a not a good way to handle this
        if hasattr(parameter_object, "fields"):
            parameter_dict: Dict[str, fields.Field] = parameter_object.fields
        else:
            parameter_dict: Dict[str, fields.Field] = parameter_object

        location_argmaps: Dict[str, Dict[str, fields.Field]] = {}
        for name, field in parameter_dict.items():
            location: str = field.metadata.get("location", "query")
            if location not in location_argmaps:
                location_argmaps[location] = {}

            location_argmaps[location][name] = field

        # TODO: clean up this code once I'm sure of not needing it
        # location_schemas: Dict[str, Union[Dict[str, Schema], type]] = {}
        # for loc, argmap in location_argmaps.items():
        #     if loc not in location_schemas:
        #         location_schemas[loc] = {}
        #     # TODO: Source a better Schema Name
        #     url_name: str = "".join([part.title() for part in path_url.split("/")])
        #     schema_name: str = f"{url_name}{http_verb.title()}{loc.title()}Schema"
        #     location_schemas[loc] = Schema.from_dict(argmap, name=schema_name)
        # class ParameterSchema(Schema):
        #     class Meta:
        #         include = {
        #             loc: fields.Nested(schema, location=loc, name=loc)
        #             for loc, schema
        #             in location_schemas.items()
        #         }

        return location_argmaps

    # TODO: nicer return than tuple
    @staticmethod
    def parse_response_schema(response_interface: Union[ResponseObjectInterface, Type[ResponseObjectInterface]],
                              path_url: str,
                              http_verb: str) -> Tuple[Schema, str]:
        """

        :param response_interface:
        :param path_url:
        :param http_verb:
        :return: Response Schema, content-type
        """
        response_schema: Schema
        if response_interface is not None:
            response_schema = response_interface.to_schema()
        else:
            url_name: str = "".join([part.title() for part in path_url.split("/")])
            # TODO: test this code path
            response_schema = Schema.from_dict({}, name=f"{url_name}{http_verb.title()}ResponseSchema")()

        content_type: str
        try:
            content_type = response_interface.content_type()
        except AttributeError:
            content_type = mimetypes.MimeTypes().types_map[1][".txt"]

        return response_schema, content_type

    def register_path(self,
                      api_spec: APISpec,
                      path_url: str,
                      http_verb: str,
                      response_code: int,
                      summary: str = None,
                      description: str = None,
                      parameter_object: Union[Dict, Schema] = None,
                      response_object: Union[Type, ResponseObjectInterface] = None,
                      func_signature: Signature = None,
                      tags: List[str] = None) -> APISpec:
        """
        Register a new path to the provided APISpec object (passed in APISpec object is mutated).
        :param api_spec: APISpec to register the path to
        :param path_url: url of the path
        :param http_verb:
        :param response_code:
        :param summary:
        :param description:
        :param parameter_object: HTTP Parameters of the path
        :param response_object: HTTP response information
        :param func_signature: inspection Signature object of the API call function
        :param tags: Tags for categorizing the path.  Defaults to the AutoMD App Title
        :return: The same APISpec object passed in, but now with a new path registered
        """

        parameter_schema: Dict = self.parse_parameter_schema(parameter_object, func_signature, path_url, http_verb)

        response_schema, content_type = self.parse_response_schema(response_object, path_url, http_verb)

        summary = summary or path_url

        verb_dict: Dict = {
            "responses": {
                str(response_code): {
                    "description": responses[response_code],
                    "content": {
                        content_type: {
                            "schema": response_schema
                        }
                    }
                }
            },
            "summary": summary,
            "tags": tags or [self.default_tag]
        }

        if description is not None:
            verb_dict["description"] = description

        resp_params = self._ma_plugin.converter.fields2parameters((parameter_schema or {}).get("query", {}),
                                                                  default_in="query")

        verb_dict["parameters"] = resp_params
        if parameter_schema:
            req_body = self._ma_plugin.converter.fields2parameters((parameter_schema or {}).get("json", {}),
                                                                   default_in="body")

            if len(req_body) > 0:
                verb_dict["requestBody"] = {
                    "content": {
                        "application/json": {
                            "schema": req_body[0]["schema"]
                        }
                    }
                }

        operations: Dict = {http_verb.lower(): verb_dict}

        api_spec.path(
            path=path_url,
            operations=operations,
        )

        return api_spec

    def application_to_apispec(self, app: Union[Flask, LocalProxy]) -> APISpec:
        """
        Create a new APISpec of the provided application that has been initialized with AutoMD
        :param app: Flask app initialized with AutoMD
        :return:
        """
        automd_spec: APISpec = self.start_spec()

        name: str
        for name, view in app.view_functions.items():
            if hasattr(view, "methods"):
                self.parse_flask_restful(automd_spec, view)
            elif hasattr(view, AutoMDKeys.function.value) or self.always_document:
                self.parse_flask_route(app, automd_spec, name, view)
            else:
                continue

        return automd_spec

    def parse_flask_route(self, app: Union[Flask, LocalProxy], automd_spec: APISpec, name: str, view):
        route_rules: List[Rule] = list(app.url_map.iter_rules(name))

        rule: Rule
        for rule in route_rules:
            method: str
            for method in rule.methods:
                if HTTPVerb[method.lower()] not in self.documented_verbs:
                    continue
                try:
                    key: str = url_for(rule.endpoint)
                except BuildError:
                    continue
                value_func: Callable = view

                if (self.always_document
                        and not hasattr(value_func, AutoMDKeys.function.value)
                        and not hasattr(value_func, AutoMDKeys.hide_function.value)):
                    value_func = automd()(value_func)

                if hasattr(value_func, AutoMDKeys.function.value):
                    automd_spec_parameters: Dict = getattr(value_func, AutoMDKeys.function.value)
                    response_schemas: Dict = automd_spec_parameters.get("response_schemas")
                    parameter_schema: Dict = automd_spec_parameters.get("parameter_schema")
                    func_signature: Signature = automd_spec_parameters.get("func_signature")
                    summary: str = automd_spec_parameters.get("summary")
                    description: str = automd_spec_parameters.get("description")
                    tags: List[str] = automd_spec_parameters.get("tags")

                    for response_code, response in response_schemas.items():
                        self.register_path(automd_spec,
                                           key,
                                           method,
                                           response_code,
                                           summary,
                                           description,
                                           parameter_schema,
                                           response,
                                           func_signature,
                                           tags)

    def parse_flask_restful(self, automd_spec: APISpec, view):
        method: str
        for method in view.methods:
            if HTTPVerb[method.lower()] not in self.documented_verbs:
                continue
            key: str = url_for(view.view_class.endpoint)

            value_func: Callable = getattr(view.view_class, method.lower())

            if (self.always_document
                    and not hasattr(value_func, AutoMDKeys.function.value)
                    and not hasattr(value_func, AutoMDKeys.hide_function.value)):
                value_func = automd()(value_func)

            if hasattr(value_func, AutoMDKeys.function.value):
                automd_spec_parameters: Dict = getattr(value_func, AutoMDKeys.function.value)
                response_schemas: Dict = automd_spec_parameters.get("response_schemas")
                parameter_schema: Dict = automd_spec_parameters.get("parameter_schema")
                func_signature: Signature = automd_spec_parameters.get("func_signature")
                summary: str = automd_spec_parameters.get("summary")
                description: str = automd_spec_parameters.get("description")
                tags: List[str] = automd_spec_parameters.get("tags")

                for response_code, response in response_schemas.items():
                    self.register_path(automd_spec,
                                       key,
                                       method,
                                       response_code,
                                       summary,
                                       description,
                                       parameter_schema,
                                       response,
                                       func_signature,
                                       tags)
