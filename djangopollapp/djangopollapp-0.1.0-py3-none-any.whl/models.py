import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


# Unique id model generated for guest users
class ClientsID(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    date_create = models.DateTimeField(
        _('Date of creation'),
        auto_now_add=True,
    )

    def __str__(self):
        return 'Guest %s' % str(self.unique_id)


# Polls model
class Polls(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Poll author',
    )
    title = models.CharField(
        _('Title of poll'),
        max_length=256,
    )
    start_date = models.DateTimeField(
        _('Poll start date'),
        auto_now_add=True,
    )
    end_date = models.DateTimeField(
        _('Poll end date')
    )
    description = models.TextField(
        _('Poll description')
    )
    members = models.ManyToManyField(
        ClientsID,
        blank=True,
        verbose_name='Members',
    )

    @property
    def is_active(self):
        now = self.start_date.now().timestamp() - self.start_date.timestamp()
        end = self.end_date.timestamp() - self.start_date.timestamp()
        if now > end: return False
        else: return True

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')


# Questions model
class Questions(models.Model):
    TYPE_CHOICES = (
        (1, _("Text answer")),
        (2, _("Single choice")),
        (3, _("Multi choice"))
    )

    poll = models.ForeignKey(Polls, on_delete=models.CASCADE)
    qns = models.CharField(
        _('Question'),
        max_length=256,
    )
    qns_type = models.IntegerField(choices=TYPE_CHOICES, default=3)

    def __str__(self):
        return self.qns

    class Meta:
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


# Text answers model for the questions
class TextAnswer(models.Model):
    qns = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.TextField(
        _('Answer text')
    )
    author = models.ForeignKey(
        ClientsID,
        on_delete=models.CASCADE,
        verbose_name='Answer author',
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Text Answer')
        verbose_name_plural = _('Text Answers')


# Choices model for the questions
class Choices(models.Model):
    qns = models.ForeignKey(Questions, on_delete=models.CASCADE)
    text = models.CharField(
        _('Choice text'),
        max_length=256,
    )
    votes = models.ManyToManyField(
        ClientsID,
        verbose_name='Votes',
        blank=True,
    )

    @property
    def vote_counter(self):
        return self.votes.count()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('Choice text')
        verbose_name_plural = _('Choice text')