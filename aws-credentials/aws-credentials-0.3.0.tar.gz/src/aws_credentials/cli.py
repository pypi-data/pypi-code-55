import argparse
import os

from .manager import Manager


def main(args=None) -> None:
    parser = argparse.ArgumentParser(
        description='Utility for managing AWS access keys.',
    )

    sub_parsers = parser.add_subparsers(
        title='Commands',
    )
    parser_activate = sub_parsers.add_parser(
        'activate',
        help='Activate a specific access key.',
        description=cmd_activate.__doc__,
    )
    add_global_options(parser_activate)
    parser_activate.add_argument(
        'access_key_id',
        help='id of the key to activate.'
    )
    parser_activate.set_defaults(_func=cmd_activate)

    parser_create = sub_parsers.add_parser(
        'create',
        help='Create a new access key.',
        description=cmd_create.__doc__,
    )
    add_global_options(parser_create)
    parser_create.set_defaults(_func=cmd_create)

    parser_deactivate = sub_parsers.add_parser(
        'deactivate',
        help='Deactivate a specific access key.',
        description=cmd_deactivate.__doc__,
    )
    add_global_options(parser_deactivate)
    parser_deactivate.add_argument(
        'access_key_id',
        help='id of the key to deactivate.'
    )
    parser_deactivate.set_defaults(_func=cmd_deactivate)

    parser_delete = sub_parsers.add_parser(
        'delete',
        help='Delete a specific access key.',
        description=cmd_delete.__doc__,
    )
    add_global_options(parser_delete)
    parser_delete.add_argument(
        'access_key_id',
        help='id of the key to delete.'
    )
    parser_delete.set_defaults(_func=cmd_delete)

    parser_list = sub_parsers.add_parser(
        'list',
        help='List access keys.',
        description=cmd_list.__doc__,
    )
    add_global_options(parser_list)
    parser_list.set_defaults(_func=cmd_list)

    parser_rotate = sub_parsers.add_parser(
        'rotate',
        help='Rotate AWS credentials.',
        description=cmd_rotate.__doc__,
    )
    add_global_options(parser_rotate)
    parser_rotate.set_defaults(_func=cmd_rotate)

    parsed_args = parser.parse_args(args)
    init_logging(parsed_args)
    try:
        parsed_args._func(parsed_args)
    except AttributeError:
        parser.print_help()


def add_global_options(parser: argparse.ArgumentParser) -> None:
    add_logging_options(parser)
    add_aws_options(parser)


def add_logging_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-v',
        '--verbose',
        help='Increase the verbosity of messages. "-v" for normal output, and "-vv" for more verbose output.',
        action='count',
        default=0,
    )


def add_aws_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '--aws-access-key-id',
        help='AWS_ACCESS_KEY_ID to use.',
        default=os.environ.get('AWS_ACCESS_KEY_ID'),
    )
    parser.add_argument(
        '--aws-secret-access-key',
        help='AWS_SECRET_ACCESS_KEY to use.',
        default=os.environ.get('AWS_SECRET_ACCESS_KEY'),
    )
    parser.add_argument(
        '--aws-session-token',
        help='AWS_SESSION_TOKEN to use.',
        default=os.environ.get('AWS_SESSION_TOKEN'),
    )


def init_logging(args: argparse.Namespace) -> None:
    import logging
    try:
        from termcolor import colored
    except ImportError:
        def colored(text, *args, **kwargs):
            return text

    try:
        if args.verbose is None:
            return
    except AttributeError:
        return
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose == 2:
        level = logging.DEBUG
    else:
        level = logging.WARNING

    fmt = colored(
        '%(levelname)-8s %(asctime)s [%(name)s] %(filename)s:%(lineno)-3s',
        'cyan'
    ) + colored(
        ' %(funcName)s',
        'yellow'
    ) + ' %(message)s'

    logging.basicConfig(
        level=level,
        format=fmt,
    )


def gitlab_issue_url(subject: str, body: str) -> str:
    from urllib.parse import urlencode
    params = urlencode({
        'issue[title]': subject,
        'issue[description]': body,
    })
    url = "https://gitlab.com/perobertson/aws-credentials/issues/new?{params}".format(
        params=params
    )
    return url


def warn_unexpected_response(action: str, response: dict) -> None:
    subject = "Unexpected response for {action}".format(
        action=action
    )
    body = "Response from AWS: `{response}`".format(
        response=response
    )
    url = gitlab_issue_url(subject, body)
    msg = 'WARNING: Unexpected response from AWS. '\
          'Please consider opening an issue with the response details.\n\n'\
          "{url}".format(url=url)
    print(msg)


def cmd_activate(args: argparse.Namespace) -> None:
    """Activate a specific access key."""
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    response = mgr.activate(args.access_key_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Activated {access_key}".format(access_key=args.access_key_id))
    else:
        warn_unexpected_response('activate', response)


def cmd_create(args: argparse.Namespace) -> None:
    """Create a new access key."""
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    response = mgr.create()
    key = response['AccessKey']
    msg = "UserName:        {}\n"\
          "AccessKeyId:     {}\n"\
          "SecretAccessKey: {}".format(
              key['UserName'],
              key['AccessKeyId'],
              key['SecretAccessKey'])
    print(msg)


def cmd_deactivate(args: argparse.Namespace) -> None:
    """Deactivate a specific access key."""
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    response = mgr.deactivate(args.access_key_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deactivated {access_key}".format(access_key=args.access_key_id))
    else:
        warn_unexpected_response('deactivate', response)


def cmd_delete(args: argparse.Namespace) -> None:
    """Delete a specific access key."""
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    response = mgr.delete(args.access_key_id)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("Deleted {access_key}".format(access_key=args.access_key_id))
    else:
        warn_unexpected_response('delete', response)


def cmd_list(args: argparse.Namespace) -> None:
    """List access keys."""
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    keys = mgr.keys()
    headers = 'AccessKeyId', 'Status', 'CreateDate'
    print("{:20} {:8} {}".format(*headers))
    for key in keys:
        print("{} {:8} {}".format(
            key['AccessKeyId'],
            key['Status'],
            key['CreateDate']
        ))


def cmd_rotate(args: argparse.Namespace) -> None:
    """Rotate AWS credentials.

    This will delete inactive keys before creating the new key.
    It will then deactivate the old key.
    """
    mgr = Manager(
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        aws_session_token=args.aws_session_token,
    )
    response = mgr.rotate()

    deleted = response.get('deleted_key')
    if deleted:
        deleted_key = deleted['AccessKey']['AccessKeyId']
    else:
        deleted_key = 'N/A'
    deactivated = response.get('deactivated_key')
    if deactivated:
        deactivated_key = deactivated['AccessKey']['AccessKeyId']
    else:
        deactivated_key = 'N/A'

    key = response['new_key']['AccessKey']
    new_key = "UserName:        {}\n"\
              "AccessKeyId:     {}\n"\
              "SecretAccessKey: {}".format(key['UserName'], key['AccessKeyId'], key['SecretAccessKey'])

    msg = """Deleted Key
-----------
{deleted}

Deactivated Key
---------------
{deactivated}

New Key
-------
{new}
""".format(
        deleted=deleted_key,
        deactivated=deactivated_key,
        new=new_key,
    )
    print(msg)
