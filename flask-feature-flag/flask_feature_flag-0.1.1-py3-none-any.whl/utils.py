import click
from constants_and_utils.utils.use_cases import Response


def response_not_found() -> tuple:
    """Function not found

    Returns:
        response (tuple): status message
    """
    return dict(message='NOT_FOUND'), 404


def response_command() -> None:
    """Function command disabled

    Returns:
        None:
    """
    click.echo('command disabled')


def response_use_case() -> Response:
    """Response use case

    Returns:
        Response:
    """
    return Response(http_code=404)
