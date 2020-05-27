import inspect
from inspect import Signature
from typing import Callable, Dict, List

from automd.keys import AutoMDKeys
from automd.responses.responses import map_response_object_type


def automd(parameter_schema: Dict = None,
           summary: str = None,
           description: str = None,
           tags: List[str] = None) -> Callable:
    """
    Decorator to perform documentation introspection on a Flask-RESTful Resource Class.
    :param parameter_schema: same as get passed into use_kwargs
    :param summary: Quick overview of the endpoint
    :param description: Detailed information about the endpoint
    :param tags: Controls which section the documentation is shown in
    :return:
    """
    def automd_wrapper(func: Callable) -> Callable:
        return_type = map_response_object_type(inspect.signature(func).return_annotation)

        automd_spec_parameters = {}

        if summary is not None:
            automd_spec_parameters["summary"] = summary

        if description is not None:
            automd_spec_parameters["description"] = description

        if tags is not None:
            automd_spec_parameters["tags"] = tags

        automd_spec_parameters["parameter_schema"] = parameter_schema

        # TODO: use signature args as fallback for schema and default values,
        #       and primary for return type, handle None return type
        automd_spec_parameters["func_signature"] = inspect.signature(func)

        automd_spec_parameters["response_schemas"] = {
            200: return_type
        }

        setattr(func, AutoMDKeys.function.value, automd_spec_parameters)

        return func
    return automd_wrapper


def disable_automd() -> Callable:
    """
    Explicitly disables AutoMD from inspecting the route, overriding "Always Document" settings.
    :return:
    """
    def automd_wrapper(func: Callable) -> Callable:
        setattr(func, AutoMDKeys.hide_function.value, True)

        return func
    return automd_wrapper


def override_webargs_flaskparser():
    import webargs.flaskparser as fp

    def automd_use_args(argmap,
                        req=None,
                        *args,
                        location=None,
                        as_kwargs=False,
                        validate=None,
                        error_status_code=None,
                        error_headers=None):
        for arg in argmap.values():
            arg.metadata["location"] = location

        parser_args: Dict = {
            "as_kwargs": as_kwargs,
            "validate": validate,
            "error_status_code": error_status_code,
            "error_headers": error_headers
        }

        flask_parser_signature: Signature = inspect.signature(fp.parser.use_args)
        if "location" in flask_parser_signature.parameters.keys():
            parser_args["location"] = location
        if "locations" in flask_parser_signature.parameters.keys():
            parser_args["locations"] = [location]

        return fp.parser.use_args(argmap, req, *args,
                                  **parser_args)

    def automd_use_kwargs(*args, **kwargs) -> Callable:
        kwargs["as_kwargs"] = True
        return automd_use_args(*args, **kwargs)

    fp.use_args = automd_use_args
    fp.use_kwargs = automd_use_kwargs
