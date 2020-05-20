# coding: utf-8

import json

import requests
from sentry.plugins.bases.notify import NotificationPlugin

import sentry_bot
from .forms import DingDingOptionsForm





class BotPlugin(NotificationPlugin):
    """
    Sentry plugin to send error counts to  Wechat
    """
    author = 'phil.xia'
    author_url = 'https://github.com/hsia1993/sentry-dingding'
    version = sentry_bot.VERSION
    description = 'Send error counts to DingDing.'
    resource_links = [
        ('Source', 'https://github.com/hsia1993/sentry-dingding'),
        ('Bug Tracker', 'https://github.com/hsia1993/sentry-dingding/issues'),
        ('README', 'https://github.com/hsia1993/sentry-dingding/blob/master/README.md'),
    ]

    slug = 'Bot'
    title = 'Bot'
    conf_key = slug
    conf_title = title
    project_conf_form = DingDingOptionsForm

    def is_configured(self, project):
        """
        Check if plugin is configured.
        """
        return bool(self.get_option('send_url', project))

    def notify_users(self, group, event, *args, **kwargs):
        self.post_process(group, event, *args, **kwargs)

    # event model: https://github.com/getsentry/sentry/blob/master/src/sentry/eventstore/models.py
    def post_process(self, group, event, *args, **kwargs):
        """
        Process error.
        """
        if not self.is_configured(group.project):
            return

        if group.is_ignored():
            return
        send_url = self.get_option('send_url', group.project)
        title = u"New alert from {}".format(event.project.slug)
        data = {
            "msgtype": "markdown",
            "markdown": {
                "content": u"#### {title} \n > {eventTitle} {message} [link]({url})".format(
                    title=title,
                    eventTitle=event.title,
                    message=event.message,
                    url=group.get_absolute_url(),
                )
            }
        }
        requests.post(
            url=send_url,
            headers={"Content-Type": "application/json"},
            data=json.dumps(data).encode("utf-8")
        )
