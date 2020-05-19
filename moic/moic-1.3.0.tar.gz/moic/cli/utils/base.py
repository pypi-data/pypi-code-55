"""
Module for base Moic cli utils function
"""
import importlib
import os

import requests

from moic.cli import COLOR_MAP, CONF_DIR, console, logger, settings


def check_instance_is_up():
    """
    Check if the Instance is accessible or not
    """
    try:
        logger.debug(f"Check if {settings.get('instance')} is available")
        requests.get(settings.get("instance"), timeout=0.5)
    except requests.exceptions.Timeout:
        logger.warning(f"Can't join {settings.get('instance')}")
        console.print(f"[red]Can't join {settings.get('instance')}[/red]")
        exit(1)


def print_comments(comments: list, prefix: str = "", oneline: bool = False):
    if oneline:
        console.line()
    for comment in comments:
        print_comment(comment, prefix, oneline)


def print_comment(comment, prefix: str = "", oneline: bool = False):
    if not oneline:
        console.print(
            f"[grey70 italic]{comment.id} [/grey70 italic][yellow]{comment.author}[/yellow] - [grey70]{comment.created}[/grey70]"
        )
        console.line()
        for line in comment.body:
            console.print(line)
        console.line()
    else:
        oneline_comment = comment.body[0]
        console.print(
            f"[grey70 italic]{comment.id} [/grey70 italic][yellow]{comment.author}[/yellow] - [grey70]{comment.created}[/grey70] : {oneline_comment} ..."
        )


def print_issues(issues: list, prefix: str = "", oneline: bool = False, subtasks: bool = False,) -> None:
    """
    Print issue list

    Args:
        issues (list): List of issues to print
        prefix (str): Prefix to display before each issue line
        oneline (bool): If set to true each issue will be printed on one line
        subtasks (bool): If set to true it will display the issue's subtasks

    Returns:
        None
    """
    for i in issues:
        if not oneline:
            console.print()
        print_issue(i, prefix=prefix, oneline=oneline, subtasks=subtasks, last=True if i == issues[-1] else False)


# TODO: Add MR print : Can't be implemented
def print_issue(issue, prefix: str = "", oneline: bool = False, subtasks: bool = False, last: bool = True) -> None:
    """
    Print an issue

    Args:
        issue : Issue to print
        prefix (str): Prefix to display before each issue line
        oneline (bool): If set to true each issue will be printed on one line
        subtasks (bool): If set to true it will display the issue's subtasks

    Returns:
        None
    """
    url = settings.get("instance") + "/browse/"
    status_color = COLOR_MAP[issue.status.color]
    if oneline:
        console.print(
            f"[{status_color}]{prefix}{issue.key}[/{status_color}] {issue.summary} [bright_black]{url}{issue.key}[/bright_black]",
            highlight=False,
        )
        if subtasks:
            sorted_subs = sort_issue_per_status(issue.subtasks)
            for sub in sorted_subs:
                prefix = "   " if last else " │ "
                prefix = f"{prefix} └─ " if sub == sorted_subs[-1] else f"{prefix} ├─ "
                print_issue(sub, prefix=prefix, oneline=True)

    else:
        console.print("key".ljust(15) + f" : {issue.key}", highlight=False)
        console.print("type".ljust(15) + f" : {issue.type.name}", highlight=False)
        console.print(
            "status".ljust(15) + f" : [{status_color}]{issue.status.name}[/{status_color}]", highlight=False,
        )
        console.print("summary".ljust(15) + f" : {issue.summary}", highlight=False)
        console.print("reporter".ljust(15) + f" : {issue.reporter}", highlight=False)
        console.print("assignee".ljust(15) + f" : {issue.assignee}", highlight=False)
        console.print("peer".ljust(15) + f" : {issue.peer}", highlight=False)
        console.print(
            "link".ljust(15) + f" : [bright_black]{url}{issue.key}[/bright_black]", highlight=False,
        )
        if subtasks:
            sorted_subs = sort_issue_per_status(issue.subtasks)
            console.print("subtasks".ljust(15) + " :")
            for sub in sorted_subs:
                status_name = sub.status.name.ljust(9)
                prefix = " └─ " if sub == sorted_subs[-1] else " ├─ "
                print_issue(sub, prefix=f" {prefix} {status_name} | ", oneline=True)


def print_status(status) -> None:
    """
    Print a Status

    Args:
        status: Status to print

    Returns:
        None
    """
    display = [f"[bold {COLOR_MAP[s.color]}]{s.name}[/bold {COLOR_MAP[s.color]}]" for s in status]
    console.print(" / ".join(display))


def sort_issue_per_status(issues: list, project: str = settings.get("default_project", None)) -> list:
    """
    Sort an issue liste based on the project defined workflow
    It will call the dedicated plugin function

    Args:
        issues (list): The list of issues to sort
        project (str): The project key

    Returns:
        list: The sorted issues list
    """
    try:
        module = importlib.import_module(f"moic.plugins.{settings.get('plugin')}.utils")
        func = getattr(module, "sort_issue_per_status")
        return func(issues, project)
    except ModuleNotFoundError:
        return issues
    except AttributeError:
        return issues


def get_template(project: str, type: str) -> str:
    """
    Get template for a given project and type

    Args:
        project (str): A project name
        type (str): A issue type name

    Returns:
        str: Path to the corresponding template
    """
    if os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/{project}_{type}")):
        return f"{CONF_DIR}/templates/{project}_{type}"
    elif os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/all_{type}")):
        return f"{CONF_DIR}/templates/{project}_{type}"
    elif os.path.isfile(os.path.expanduser(f"{CONF_DIR}/templates/all_all")):
        return f"{CONF_DIR}/templates/all_all"
    else:
        return None


def get_plugin_command(command: str, method: str):
    """
    Get a command from a plugin base on the plugin name
    If the command or the method in the command doesn't exists, it will exit with a error message

    Args:
        command (str): The command group used
        method (str): The command inside the group

    Returns:
        func: The function which should be called
    """
    try:
        logger.debug(f"- Get '{command} {method}' command from '{settings.get('plugin')}' plugin")
        module = importlib.import_module(f"moic.plugins.{settings.get('plugin')}.commands.{command}")
        func = getattr(module, method)
        return func
    except ModuleNotFoundError:
        console.print(f"[red]Plugin {settings.get('plugin')} doesn't provide a {command} command")
        exit(1)
    except AttributeError:
        console.print(f"[red]Plugin {settings.get('plugin')} {command} command doesn't provide a {method} subcommand")
        exit(1)


def get_plugin_custom_commands(plugin: str):
    """
    Get the list of custom commands and custom group defined in the plugin

    Args:
        plugin (str): Plugin name

    Returns:
        list: List of custom command to add to Moic
    """
    try:
        module = importlib.import_module(f"moic.plugins.{plugin}")
        custom_commands_list = getattr(module, "custom_commands")
        cc_list = []
        for command in custom_commands_list:
            try:
                m = ".".join(command.split(".")[:-1])
                f = command.split(".")[-1:][0]
                custom_command_module = importlib.import_module(f"moic.plugins.{plugin}.commands.{m}")
                func = getattr(custom_command_module, f)
                cc_list.append(func)
            except ModuleNotFoundError:
                console.print(f"[red]Plugin {plugin} doesn't provide a custom command {command}")
                exit(1)
            except AttributeError:
                console.print(f"[red]Plugin {plugin} doesn't provide a custom subcommand {f} for command {m}")
                exit(1)
        return cc_list
    except ModuleNotFoundError:
        console.print(f"[red]Plugin {plugin} doesn't exists")
        exit(1)
    except AttributeError:
        return []


def get_plugin_validator(validator: str):
    """
    Get the validator corresponding to the resource type within the given plugin

    Args:
        validator (str): The validator type name

    Return:
        func: The validator function
    """
    try:
        logger.debug(f"- Get '{validator}' validator from '{settings.get('plugin')}' plugin")
        module = importlib.import_module(f"moic.plugins.{settings.get('plugin')}.validators")
        func = getattr(module, f"validate_{validator}")
        return func
    except ModuleNotFoundError:
        return None
    except AttributeError:
        return None


def get_plugin_autocomplete(autocompleter: str):
    """
    Get the autocomplete method corresponding to the resource type within the given plugin

    Args:
        autocompleter (str): Resource name to autocomplete

    Return:
        func: The autocompletion function
    """
    try:
        logger.debug(f"- Get '{autocompleter}' autocompletion from '{settings.get('plugin')}' plugin")
        module = importlib.import_module(f"moic.plugins.{settings.get('plugin')}.completion")
        func = getattr(module, f"autocomplete_{autocompleter}")
        return func
    except ModuleNotFoundError:
        return None
    except AttributeError:
        return None


def get_plugin_instance(plugin: str):
    """
    Get the instance class within the given plugin

    Args:
        plugin (str): Plugin name

    Return:
        class: The plugin Instance
    """
    try:

        logger.debug(f"- Get 'Instance' class from '{settings.get('plugin')}' plugin")
        module = importlib.import_module(f"moic.plugins.{plugin}")
        func = getattr(module, "Instance")
        return func
    except ModuleNotFoundError:
        console.print(f"[red]Plugin {plugin} doesn't exists")
        exit(1)
    except AttributeError:
        console.print(f"[red]Plugin {plugin} doesn't provide an Instance class")
        exit(1)
