# Copyright (c) 2014-2020 GeoSpock Ltd.

import click
import json
import boto3

from geospock_cli.auth import Authorizer
from geospock_cli.exceptions import CLIError
from geospock_cli.config_reader import ConfigReaderAndWriter
from geospock_cli.message_sender import MessageSender
from pkg_resources import resource_string
from typing import Tuple
from urllib.parse import urlparse


def get_header(config_reader: ConfigReaderAndWriter) -> Tuple[dict, str]:
    config_all = config_reader.get_config()
    if config_reader.profile not in config_all and config_reader.profile != "default":
        raise CLIError(ConfigReaderAndWriter.MESSAGES["profileError"].format(config_reader.profile))
    elif config_reader.profile not in config_all:
        raise CLIError(ConfigReaderAndWriter.MESSAGES["noInit"].format(config_reader.profile))
    request_address = config_reader.config["request_address"]
    all_credentials = config_reader.get_all_credentials_from_file()
    auth = Authorizer(config_reader)
    if all_credentials is None or config_reader.profile not in all_credentials:
        credentials = auth.init_credentials()
    else:
        credentials = auth.renew_credentials()

    if credentials:
        headers = {"content-type": "application/json", "authorization": "Bearer " + credentials["access_token"]}
        return headers, request_address
    else:
        raise CLIError(ConfigReaderAndWriter.MESSAGES["invalidCredentials"])


def display_result(result: dict, output_object: str, is_stringified_json: bool) -> None:
    try:
        if output_object and is_stringified_json:
            output_dict = dict()
            for item in result["data"][output_object]:
                try:
                    output_dict[item] = json.loads(result["data"][output_object][item])
                except json.JSONDecodeError:
                    output_dict[item] = result["data"][output_object][item]
            click.echo(json.dumps(output_dict, indent=4))
        elif output_object:
            click.echo(json.dumps(result["data"][output_object], indent=4))
        else:
            click.echo(json.dumps(result["data"], indent=4))
    except json.JSONDecodeError:
        raise CLIError("Error in response from server: {}".format(result))
    except Exception:
        raise CLIError(ConfigReaderAndWriter.MESSAGES["graphQLError"] + str(result))


def clean_null_items(input):
    if isinstance(input, dict):
        clean = dict()
        for key, value in input.items():
            clean_value = clean_null_items(value)
            if value is not None:
                clean[key] = clean_value
        return clean
    elif isinstance(input, list):
        new_list = []
        for item in input:
            new_list.append(clean_null_items(item))
        return new_list
    return input


def display_result_without_nulls(result: dict, output_object: str) -> None:
    try:
        if output_object:
            new_output = clean_null_items(result["data"][output_object])
            click.echo(json.dumps(new_output, indent=4))
        else:
            click.echo(json.dumps(result["data"], indent=4))
    except json.JSONDecodeError:
        raise CLIError("Error in response from server: {}".format(result))
    except Exception:
        raise CLIError(ConfigReaderAndWriter.MESSAGES["graphQLError"] + str(result))


def init(config_reader, clientid, audience, auth0url, request_address) -> None:
    config_reader.write_to_config(clientid, audience, auth0url, request_address)
    click.secho(ConfigReaderAndWriter.MESSAGES["nowGetCredentials"].format(" --profile " + config_reader.profile
                                                    if config_reader.profile != "default" else ""), fg="green")


@click.command(help=ConfigReaderAndWriter.MESSAGES["helpRun"], context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.pass_context
@click.argument('command')
@click.option('--profile', default="default", help=ConfigReaderAndWriter.MESSAGES["profileText"])
@click.option('--debug', is_flag=True, help=ConfigReaderAndWriter.MESSAGES["debugText"])
@click.option('--no-browser', is_flag=True, help=ConfigReaderAndWriter.MESSAGES["noBrowserText"])
def run(ctx, command, profile, debug, no_browser) -> None:
    try:
        config_reader = ConfigReaderAndWriter(profile, not no_browser)
        if command == "help" and len(ctx.args) == 0:
            help_all(config_reader, debug)
        elif command == "help":
            help_command(config_reader, ctx.args[0], debug)
        elif command == "profile-list":
            profile_list(config_reader)

        # We want the number of additional arguments to be even (i.e. number % 2 == 0) so that every {--argumentName}
        # corresponds to an {argumentValue}
        elif len(ctx.args) % 2 != 0:
            click.echo(ConfigReaderAndWriter.MESSAGES["argNumberWrong"])
        else:
            args = {ctx.args[i][2:]: ctx.args[i + 1] for i in range(0, len(ctx.args), 2)}
            if command == "init":
                # Saving info to config.json
                try:
                    init(config_reader, args["clientid"], args["audience"], args["auth0url"], args["request-address"])
                except KeyError:
                    raise CLIError(ConfigReaderAndWriter.MESSAGES["helpInit"])
            elif command == "get-credentials":
                # Add to credentials file
                if get_header(config_reader):
                    click.secho("Credentials saved", fg="green")
            else:
                run_command(command, config_reader, args, debug)
    except CLIError as e:
        click.secho(str(e.message), fg="red")
        exit(e.exit_code)


def load_file(address):
    if address.startswith("s3://") or address.startswith("S3://"):
        parsed_url = urlparse(address)
        s3 = boto3.resource("s3")
        try:
            obj = s3.Object(parsed_url.netloc, parsed_url.path[1:])
            file_contents = obj.get()['Body'].read().decode()
            return json.loads(file_contents)
        except s3.meta.client.exceptions.NoSuchKey:
            raise CLIError("File {} does not exist.".format(address))
        except json.JSONDecodeError:
            raise CLIError("Error trying to read JSON in input file: {}".format(address))
    try:
        with open(address, "r") as input_file:
            return json.load(input_file)
    except FileNotFoundError:
        raise CLIError("File {} does not exist.".format(address))
    except json.JSONDecodeError:
        raise CLIError("Error trying to read JSON in input file: {}".format(address))


def run_command(command: str, config_reader: ConfigReaderAndWriter, args: dict, debug: bool) -> None:
    # Where we have an argument ending in the following, read from a file rather than taking the direct string
    file_indicator = ".json"
    response_json = get_command_from_server(config_reader, command, debug)
    if response_json is None:
        click.echo("Could not get command {} from service".format(command))
    if "error" in response_json:
        raise CLIError(response_json["error"])
    elif "responseTemplate" in response_json:
        graphql = response_json["responseTemplate"]
        internal_name = response_json["internalName"]
        parameters = response_json["parameters"]
        new_args, arg_missing = process_parameters(parameters, args, file_indicator, command)
        if not arg_missing:
            request = {"operationName": internal_name, "query": graphql, "variables": new_args}
            response_data_json = get_from_server(config_reader, request, internal_name, debug)
            if response_json.get("stripNulls", False):
                display_result_without_nulls(response_data_json, internal_name)
            else:
                display_result(response_data_json, internal_name, response_json.get("returnsStringifiedJson", False))
        else:
            raise CLIError("Required arguments missing from command", 64)
    else:
        raise CLIError("Query not found")


def process_parameters(parameters: dict, args: dict, file_indicator: str, command: str) -> Tuple[dict, bool]:
    new_args = dict()
    arg_missing = False
    for parameter in parameters:
        if (parameter["name"] in args and parameter["type"] in ["String", "Int", "ID", "Boolean"] and
                ("fromFile" not in parameter or not parameter["fromFile"])):
            new_args[parameter["internalName"]] = args[parameter["name"]]
        elif parameter["name"] in args and parameter["type"] == "enum":
            if args[parameter["name"]] in parameter["enumValues"]:
                new_args[parameter["internalName"]] = args[parameter["name"]]
            else:
                arg_missing = True
                click.echo("Value {0} not allowed for argument --{1}. Allowed values: {2}".format(args[parameter["name"]],
                                                                                                  parameter["name"],
                                                                                                  parameter["enumValues"]))
        elif parameter["name"] in args \
                and args[parameter["name"]][-len(file_indicator):] == file_indicator \
                and ("fromFile" in parameter and parameter["fromFile"]) \
                and parameter["type"] == "String":
            file_contents = load_file(args[parameter["name"]])
            new_args[parameter["internalName"]] = file_contents
        elif parameter["name"] in args \
                and args[parameter["name"]][-len(file_indicator):] == file_indicator \
                and ("fromFile" in parameter and parameter["fromFile"]):
            file_contents = load_file(args[parameter["name"]])
            new_args[parameter["internalName"]] = file_contents
        elif "default" in parameter:
            new_args[parameter["internalName"]] = parameter["default"]
        elif ("subParams" in parameter and len(parameter["subParams"]) == 0) and parameter["required"]:
            click.echo("Required argument --{0} not provided for command {1}".format(parameter["name"], command))
            arg_missing = True
        elif "subParams" in parameter and len(parameter["subParams"]) > 0:
            new_args[parameter["internalName"]], sub_arg_missing = process_parameters(parameter["subParams"], args,
                                                                                      file_indicator, command)
            arg_missing = arg_missing or sub_arg_missing
        elif parameter["required"]:
            click.echo("Required argument --{0} not provided for command {1}".format(parameter["name"], command))
            arg_missing = True
    return new_args, arg_missing


def help_all(config_reader: ConfigReaderAndWriter, debug: bool) -> None:
    commands_json = get_commands_from_server(config_reader, debug)
    max_len = max([len(key) for key in commands_json])
    click.echo(ConfigReaderAndWriter.MESSAGES["helpAllCommands"])
    for command in commands_json:
        arg_list = []
        for arg in commands_json[command]["parameters"]:
            if arg["fromFile"] or len(arg["subParams"]) == 0:
                arg_list.append("--" + arg["name"] + " <value>")
            else:
                for sub_arg in arg["subParams"]:
                    arg_list.append("--" + sub_arg["name"] + " <value>")
        if len(arg_list) == 0:
            click.echo("{value:>{width}}".format(value=command, width=max_len))
        else:
            click.echo("{value:>{width}}".format(value=command, width=max_len) + " " + arg_list[0])
            for arg in arg_list[1:]:
                click.echo(" " * (max_len + 1) + arg)
        click.echo()


def help_command(config_reader: ConfigReaderAndWriter, command: str, debug: bool) -> None:
    command_json = get_command_from_server(config_reader, command, debug)
    if command_json and "error" in command_json:
        raise CLIError(command_json["error"])
    elif command_json:
        click.secho("NAME", bold=True)
        click.echo("\t" + command)
        click.secho("\nDESCRIPTION", bold=True)
        click.echo("\t" + command_json["description"])
        if command_json["internalCommand"]:
            click.secho("\t" + ConfigReaderAndWriter.MESSAGES["internalCommand"], fg="yellow")
        click.secho("\nOPTIONS", bold=True)
        if len(command_json["parameters"]) == 0:
            click.echo("\t" + ConfigReaderAndWriter.MESSAGES["noArgsNeeded"])
        for arg in command_json["parameters"]:
            if arg["fromFile"] or len(arg["subParams"]) == 0:
                output_arg(arg)
            else:
                for sub_arg in arg["subParams"]:
                    output_arg(sub_arg)
    else:
        click.echo("Command {} not recognised.".format(command))


def output_arg(arg: dict) -> None:
    click.echo(f'\t--{arg["name"]}: {arg["type"]}'
               + (f' (optional)' if not arg["required"] else "")
               + (f' (default: " + str(sub_arg["default"]) + ")' if "default" in arg else '')
               + (f' Allowed values: {str(arg["enumValues"])}' if arg["type"] == "enum" else ''))


def profile_list(config_reader: ConfigReaderAndWriter) -> None:
    all_configs = config_reader.get_config()
    click.echo("Initialised profiles: ")
    for profile in all_configs:
        click.echo(f"--profile {profile}")


def get_from_server(config_reader: ConfigReaderAndWriter, request: dict, object_name: str, debug) -> dict:
    header, request_address = get_header(config_reader)

    if header:
        try:
            response = MessageSender.parse_and_make_request(request_address, "POST", json.dumps(request), header)
            response_json = json.loads(response)
            if "errors" in response_json and debug:
                click.echo(json.dumps(response_json["errors"], indent=4))
                click.echo("The following data was returned in addition to the error messages above: ", nl=False)
                display_result(response_json, object_name, False)
                exit(1)
            elif "errors" in response_json:
                for error in response_json["errors"]:
                    click.secho(error["message"], fg="red")
                exit(1)
            else:
                try:
                    return json.loads(response_json["data"][object_name])
                except TypeError:
                    return response_json
        except ConnectionRefusedError:
            raise CLIError("Connection refused")
        except Exception as e:
            raise CLIError(str(e))
    else:
        raise CLIError(ConfigReaderAndWriter.MESSAGES["noHeader"])


def get_commands_from_server(config_reader: ConfigReaderAndWriter, debug: bool) -> dict:
    graphql = resource_string('geospock_cli', "graphql_templates/getCommands.graphql").decode("utf-8")
    request = {"operationName": "getCliCommands", "query": graphql, "variables": {}}
    return get_from_server(config_reader, request, "getCliCommands", debug)


def get_command_from_server(config_reader: ConfigReaderAndWriter, command: str, debug: bool) -> dict:
    graphql = resource_string('geospock_cli', "graphql_templates/getCommand.graphql").decode("utf-8")
    request = {"operationName": "getCliCommand", "query": graphql, "variables": {"commandName": command}}
    return get_from_server(config_reader, request, "getCliCommand", debug)


if __name__ == '__main__':
    run()
