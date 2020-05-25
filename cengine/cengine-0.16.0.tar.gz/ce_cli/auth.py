import click
from tabulate import tabulate  # TODO: add to requirements

import ce_api
from ce_api.models import AuthEmail
from ce_cli import constants
from ce_cli.cli import cli
from ce_cli.utils import api_client, api_call
from ce_cli.utils import check_login_status, pass_info, Info
from ce_cli.utils import declare, format_date_for_display, confirmation


@cli.group()
@pass_info
def auth(info):
    """Authentication utilities of the Core Engine"""
    pass


@auth.command()
@pass_info
def login(info):
    """Login with your username and password"""
    username = click.prompt('Please enter your email', type=str)
    password = click.prompt('Please enter your password', type=str,
                            hide_input=True)

    # API instance
    config = ce_api.Configuration()
    config.host = constants.API_HOST
    api_instance = ce_api.LoginApi(ce_api.ApiClient(config))

    output = api_call(
        func=api_instance.login_access_token_api_v1_login_access_token_post,
        username=username,
        password=password
    )

    info[constants.ACTIVE_USER] = username
    declare('Login successful!')
    if username in info:
        info[username][constants.TOKEN] = output.access_token
    else:
        info[username] = {constants.TOKEN: output.access_token}

    info.save()


@auth.command()
@pass_info
def logout(info):
    """Log out of your account"""
    if click.confirm('Are you sure that you want to log out?'):
        click.echo('Logged out!')
        info[constants.ACTIVE_USER] = None
        info.save()


@auth.command()
@click.option('--all', is_flag=True, help='Flag to reset all users')
@pass_info
def reset(info, all):
    """Reset cookies"""
    if all:
        if click.confirm('Are you sure that you want to reset for all?'):
            info = Info()
            info.save()
            click.echo('Info reset!')
        else:
            click.echo('Reset aborted!')
    else:
        active_user = info[constants.ACTIVE_USER]

        if click.confirm('Are you sure that you want to reset info for '
                         '{}?'.format(active_user)):
            info[active_user] = {}
            info.save()
            click.echo('Info reset!')
        else:
            click.echo('Reset aborted!')

        info[active_user] = {}
        info.save()


@auth.command()
@pass_info
def resetpassword(info):
    """Send reset password link to registered email address"""
    confirmation('Are you sure you want to reset your password? This will '
                 'trigger an email for resetting your password and '
                 'clear cookies.', abort=True)
    check_login_status(info)
    api = ce_api.UsersApi(api_client(info))
    user = api_call(api.get_loggedin_user_api_v1_users_me_get)
    api = ce_api.LoginApi(api_client(info))
    api_call(api.send_reset_pass_email_api_v1_login_email_resetpassword_post,
             AuthEmail(email=user.email))
    info[constants.ACTIVE_USER] = None
    info.save()
    declare("Reset password email sent to {}".format(user.email))


@auth.command()
@pass_info
def whoami(info):
    """Info about the account which is currently logged in"""
    check_login_status(info)
    api = ce_api.UsersApi(api_client(info))
    user = api_call(api.get_loggedin_user_api_v1_users_me_get)

    table = [{
        'Email': info[constants.ACTIVE_USER],
        'Name': user.full_name if user.full_name else '',
        'Pipelines Created': user.n_pipelines_created,
        'Pipelines Run': user.n_pipelines_executed,
        'Credits Remaining (€)': user.credit_remaining,
        'Credits Expiry Date': format_date_for_display(user.credit_end_time),
    }]
    click.echo(tabulate(table, headers='keys', tablefmt='presto'))
