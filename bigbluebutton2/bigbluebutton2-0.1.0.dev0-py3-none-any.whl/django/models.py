from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from django.utils.translation import gettext_lazy as _

from .. import api as bbb


class BigBlueButton(models.Model):
    name = models.CharField(verbose_name=_("Server name"), max_length=60)
    url = models.URLField(verbose_name=_("API base URL"))
    salt = models.CharField(verbose_name=_("API shared secret"), max_length=60)

    group = models.ForeignKey("BigBlueButtonGroup", on_delete=models.CASCADE, related_name="apis")

    _api = None

    @classmethod
    def from_api(cls, api: bbb.bigbluebutton.BigBlueButton, group: "BigBlueButtonGroup"):
        obj, created = cls.update_or_create(
            url=api.url, group=group, defaults={"name": api.name, "salt": api.salt}
        )
        obj.save()

        obj._api = api

        return obj

    @property
    def api(self) -> bbb.bigbluebutton.BigBlueButton:
        if self._api is None:
            if self.name in self.group.api_group.apis:
                self._api = self.group.api_group.apis["self.name"]
            else:
                self._api = bbb.bigbluebutton.BigBlueButton(
                    self.group.api_group, self.name, self.url, self.salt
                )
        return self._api


class BigBlueButtonGroup(models.Model):
    name = models.CharField(verbose_name=_("Group name"), max_length=60)

    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=Site.objects.get_current)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    _api_group = None

    @property
    def api_group(self) -> bbb.bigbluebutton.BigBlueButtonGroup:
        if self._api_group is None:
            self._api_group = bbb.bigbluebutton.BigBlueButtonGroup(
                self.name, origin=self.site.name, origin_server_name=self.site.domain
            )
        return self._api_group


class Meeting(models.Model):
    name = models.CharField(verbose_name=_("Meeting name"), max_length=60)

    welcome_message = models.TextField(verbose_name=_("Welcome message"), blank=True)
    moderator_message = models.TextField(
        verbose_name=_("Welcome message for moderators"), blank=True
    )

    max_participants = models.PositiveSmallIntegerField(
        verbose_name=_("Maximum number of participants"), default=0
    )

    api = models.ForeignKey("BigBlueButton", on_delete=models.CASCADE, related_name="meetings")

    _meeting = None

    @classmethod
    def from_api(cls, api: bbb.bigbluebutton.BigBlueButton, meeting: bbb.meeting.Meeting):
        obj, created = cls.update_or_create(
            name=meeting.meeting_name,
            api=api,
            defaults={
                "welcome_message": meeting.welcome_message,
                "moderator_message": meeting.moderator_only_message,
                "max_participants": meeting.max_participants,
            },
        )
        obj.save()

        obj._meeting = meeting

        return obj

    @property
    def meeting(self) -> bbb.meeting.Meeting:
        if self._meeting is None:
            self._meeting = self.api.api.create_meeting(
                meeting_name=self.name,
                welcome_message=self.welcome_message,
                moderator_only_message=self.moderator_message,
                max_participants=self.max_participants,
            )
        return self._meeting
