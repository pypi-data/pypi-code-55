import os

import click
import slack
from click_option_group import RequiredMutuallyExclusiveOptionGroup, optgroup


@click.command(name="files.upload", help="Uploads or creates a file. See https://api.slack.com/methods/files.upload ")
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--channels", required=True)
@optgroup.group("File contents", cls=RequiredMutuallyExclusiveOptionGroup)
@optgroup.option("--file")
@optgroup.option("--content")
@click.option("--filename")
@click.option("--filetype")
@click.option("--initial_comment")
@click.option("--thread_ts")
@click.option("--title")
def upload(token, channels, file, content, filename, filetype, initial_comment, thread_ts, title):
    client = slack.WebClient(token=token)

    if filename is None and file is not None:
        filename = os.path.basename(file)

    response = client.files_upload(
        channels=channels,
        file=file,
        content=content,
        filename=filename,
        filetype=filetype,
        initial_comment=initial_comment,
        thread_ts=thread_ts,
        title=title,
    )
    print(response)
    return response


@click.command(name="files.delete", help="Deletes a file. See https://api.slack.com/methods/files.delete ")
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--file", required=True)
def delete(token, file):
    client = slack.WebClient(token=token)
    response = client.files_delete(file=file)
    print(response)
    return response
