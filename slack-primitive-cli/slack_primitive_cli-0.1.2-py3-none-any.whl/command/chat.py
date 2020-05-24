import click
import slack


@click.command(
    name="chat.postMessage", help="Sends a message to a channel. See https://api.slack.com/methods/chat.postMessage "
)
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--channel", required=True)
@click.option("--text", required=True)
@click.option("--as_user", type=bool)
@click.option("--attachments")
@click.option("--blocks")
@click.option("--icon_emoji")
@click.option("--icon_url")
@click.option("--link_names", type=bool)
@click.option("--mrkdwn", type=bool)
@click.option("--parse", type=bool)
@click.option("--reply_broadcast", type=bool)
@click.option("--thread_ts")
@click.option("--unfurl_links", type=bool)
@click.option("--unfurl_media", type=bool)
@click.option("--username")
def postMessage(
    token: str,
    channel: str,
    text: str,
    as_user,
    attachments,
    blocks,
    icon_emoji,
    icon_url,
    link_names,
    mrkdwn,
    parse,
    reply_broadcast,
    thread_ts,
    unfurl_links,
    unfurl_media,
    username,
):
    client = slack.WebClient(token=token)
    response = client.chat_postMessage(
        channel=channel,
        text=text,
        as_user=as_user,
        attachments=attachments,
        blocks=blocks,
        icon_emoji=icon_emoji,
        icon_url=icon_url,
        link_names=link_names,
        mrkdwn=mrkdwn,
        parse=parse,
        reply_broadcast=reply_broadcast,
        thread_ts=thread_ts,
        unfurl_links=unfurl_links,
        unfurl_media=unfurl_media,
        username=username,
    )
    print(response)
    return response


@click.command(name="chat.delete", help="Deletes a message. See https://api.slack.com/methods/chat.delete ")
@click.option("--token", envvar="SLACK_API_TOKEN", required=True)
@click.option("--channel", required=True)
@click.option("--ts", required=True)
@click.option("--as_user", type=bool)
def delete(token: str, channel: str, ts: str, as_user):
    client = slack.WebClient(token=token)
    response = client.chat_delete(channel=channel, ts=ts, as_user=as_user)
    print(response)
    return response
