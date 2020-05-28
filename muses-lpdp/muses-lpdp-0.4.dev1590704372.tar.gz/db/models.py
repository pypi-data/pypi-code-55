# Create your models here.
import pytz
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from precise_bbcode.fields import BBCodeTextField

from db.validators import not_passed
from editorjs.fields import EditorJSField


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        unique=False,
        null=False,
        blank=False,
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('updated at'),
        unique=False,
        null=False,
        blank=False,
        auto_now=True
    )
    deleted_at = models.DateTimeField(
        verbose_name=_('deleted at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        abstract = True


class MemberQuerySet(models.QuerySet):
    def superusers(self):
        return self.filter(is_superuser=True)

    def staff(self):
        return self.filter(is_staff=True)

    def privileges(self):
        return self.filter(status=Member.PRIVILEGE)

    def regulars(self):
        return self.filter(status=Member.REGULAR)


class MemberManager(BaseUserManager):
    def get_queryset(self):
        return MemberQuerySet(self.model, using=self._db)

    def superusers(self):
        return self.get_queryset().superusers()

    def staff(self):
        return self.get_queryset().staff()

    def privileges(self):
        return self.get_queryset().privileges()

    def regulars(self):
        return self.get_queryset().regulars()

    def create_user(self, username, email, date_of_birth, password=None, **kwargs):
        email = MemberManager.normalize_email(email)
        if password is None:
            password = MemberManager.make_random_password(self)
        member = Member(username=username, email=email, date_of_birth=date_of_birth)
        member.set_password(password)
        for key, value in kwargs.items():
            setattr(member, key, value)
        member.clean()
        member.save()

    def create_superuser(self, username, email, date_of_birth, password=None, **kwargs):
        if password is None:
            password = MemberManager.make_random_password(self)
        member = Member(username=username, email=email, date_of_birth=date_of_birth)
        member.is_staff = True
        member.is_superuser = True
        member.set_password(password)
        for key, value in kwargs.items():
            setattr(member, key, value)
        member.clean()
        member.save()


class Member(AbstractBaseUser, PermissionsMixin, BaseModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    date_of_birth = models.DateField()
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    def member_avatar_path(self, filename):
        return 'avatars/member_{0}/{1}'.format(self.id, filename)

    avatar = models.ImageField(
        verbose_name=_('avatar'),
        upload_to=member_avatar_path,
        storage=FileSystemStorage
    )
    web_site = models.URLField(
        verbose_name=_('web site'),
        max_length=2048,
    )
    gender = models.CharField(
        verbose_name=_('gender'),
        max_length=1
    )
    occupation = models.CharField(
        verbose_name=_('occupation'),
        max_length=255
    )
    phone_number = PhoneNumberField(
        verbose_name=_('phone number'),
        blank=True
    )
    privilege_start_date = models.DateField(
        verbose_name=_('privilege start date'),
        null=True
    )
    postal_address = models.CharField(
        verbose_name=_('postal address'),
        max_length=1024
    )
    postal_address_2 = models.CharField(
        verbose_name=_('postal address 2'),
        max_length=1024
    )
    postal_city = models.CharField(
        verbose_name=_('postal city'),
        max_length=200
    )
    postal_code = models.CharField(
        verbose_name=_('postal code'),
        max_length=20
    )
    language = models.CharField(
        verbose_name=_('language'),
        max_length=2
    )
    locked = models.BooleanField(
        verbose_name=_('locked'),
        default=False
    )

    """
    ------------------------------
    *** DEBUT LISTE DES THEMES ***
    ------------------------------
    Section à compléter pour ajouter des thèmes complémentaires
    """

    THEME_DEFAULT = "muses_default"
    THEME_CLASSIC = "muses_classic"
    THEME_ROSE = "muses_rose"
    THEME_BLUE = "muses_blue"
    THEME_GREEN = "muses_green"
    THEME_ORANGE = "muses_orange"

    THEME_CHOICES = (
        (THEME_DEFAULT, _("Default")),
        (THEME_CLASSIC, _("Classic")),
        (THEME_ROSE, _("Rose")),
        (THEME_BLUE, _("Blue")),
        (THEME_GREEN, _("Green")),
        (THEME_ORANGE, _("Orange")),
    )

    """
    ------------------------------
    *** FIN LISTE DES THEMES ***
    ------------------------------
    """

    theme = models.CharField(
        verbose_name=_('theme'),
        max_length=30,
        choices=THEME_CHOICES,
        default=THEME_DEFAULT
    )

    connections_counter = models.IntegerField(
        verbose_name=_('connections counter'),
        default=0,
    )
    page_views_counter = models.IntegerField(
        verbose_name=_('page views counter'),
        default=0,
    )

    email_notification_on_new_comment = models.BooleanField(
        verbose_name=_('email notification on new comment'),
        default=False
    )
    email_notification_on_new_message = models.BooleanField(
        verbose_name=_('email notification on new message'),
        default=False
    )

    mailbox_collapsing = models.BooleanField(
        verbose_name=_('mailbox collapsing'),
        default=False
    )
    mailbox_blocked = models.BooleanField(
        verbose_name=_('mailbox blocked'),
        default=False
    )

    ALL_TIMEZONES = sorted((item, item) for item in pytz.all_timezones)
    tz_name = models.CharField(choices=ALL_TIMEZONES, max_length=64)

    story = models.TextField(
        verbose_name=_('story'),
        default="",
        unique=False,
        blank=False,
        null=False
    )

    REGULAR = 'R'
    PRIVILEGE = 'P'
    MEMBER_STATUS_CHOICES = [
        (REGULAR, 'REGULAR'),
        (PRIVILEGE, 'PRIVILEGE')
    ]
    status = models.CharField(
        verbose_name=_('status'),
        max_length=10,
        choices=MEMBER_STATUS_CHOICES,
        default=REGULAR
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth', 'email']

    blocked_contacts = models.ManyToManyField(
        to='self',
        related_name='blocked_contact'
    )

    objects = MemberManager()

    class Meta:
        verbose_name = _('member')
        verbose_name_plural = _('members')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class MessageManager(models.Manager):
    pass


class Message(BaseModel):
    subject = models.CharField(
        verbose_name=_('subject'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no subject")
    )
    content = models.TextField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    sender = models.ForeignKey(
        to=Member,
        related_name='sender_ref',
        on_delete=models.CASCADE
    )
    recipient = models.ManyToManyField(
        to=Member,
        verbose_name=_('recipient'),
        related_name='recipients',
        related_query_name='recipients'
    )
    message_box = models.ForeignKey(
        to=Member,
        related_name=_('message_box'),
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def send(self):
        pass


class SiteParamManager(models.Manager):
    pass


class SiteParam(BaseModel):
    key = models.CharField(
        verbose_name=_('key'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no name")
    )
    value = models.CharField(
        verbose_name=_("value"),
        unique=True,
        null=False,
        blank=False,
        default=_('no value'),
        db_index=True,
        max_length=2048
    )

    objects = SiteParamManager()

    class Meta:
        verbose_name = 'site parameter'
        verbose_name_plural = 'site parameters'


class SectionManager(models.Manager):
    pass


class Section(BaseModel):
    ACTIVE = 1
    DISABLED = 2
    STATUS_CHOICES = (
        (ACTIVE, _('active')),
        (DISABLED, _('disabled'))
    )
    short_name = models.CharField(
        verbose_name=_('short name'),
        unique=True,
        max_length=20,
        default=_('no short name'),
        db_index=True
    )
    name = models.CharField(
        verbose_name=_('name'),
        unique=False,
        max_length=255,
        default=_('no name'),
        db_index=True
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        unique=True,
        default=0
    )
    description = models.TextField(
        verbose_name=_('description'),
        max_length=1024,
        null=True
    )
    status = models.IntegerField(
        verbose_name=_('status'),
        choices=STATUS_CHOICES,
        default=DISABLED
    )
    groups = models.ManyToManyField(
        to=Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this section belongs to.'
        ),
        related_name="section_set",
        related_query_name="section",
    )

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')


class TagManager(models.Manager):
    pass


class Tag(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        db_index=True
    )
    enable_at = models.DateTimeField(
        verbose_name=_('enable at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True
    )
    disable_at = models.DateTimeField(
        verbose_name=_('disable at'),
        unique=False,
        null=True,
        blank=True,
        db_index=True
    )
    CATEGORY = 0
    THEME = 1
    PROSODY = 2
    FORM = 3
    USER = 4
    EVENT = 5
    TYPE_CHOICES = (
        (CATEGORY, _('category')),
        (THEME, _('theme')),
        (PROSODY, _('prosody')),
        (FORM, _('form')),
        (USER, _('user')),
        (EVENT, _('event')),
    )
    type = models.CharField(
        verbose_name=_('type'),
        unique=False,
        null=False,
        blank=True,
        db_index=False,
        max_length=255,
        choices=TYPE_CHOICES,
        default=USER
    )
    mature = models.BooleanField(
        verbose_name=_('mature'),
        unique=False,
        null=False,
        blank=True,
        default=False
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    valid_sections = models.ManyToManyField(
        to=Section
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'


class AdmonitionTemplateManager(models.Manager):
    pass


class AdmonitionTemplate(BaseModel):
    subject = models.CharField(
        verbose_name=_('subject'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no subject")
    )
    content = models.TextField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    objects = AdmonitionTemplateManager()


class LicenseManager(models.Manager):
    pass


class License(BaseModel):
    name: str = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=True
    )
    text = models.TextField(
        verbose_name=_('text'),
        null=True
    )
    logo = models.ImageField(
        verbose_name=_('logo'),
        null=True
    )
    active = models.BooleanField(
        verbose_name=_('active'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    def __str__(self):
        return self.name

    objects = LicenseManager()

    class Meta:
        verbose_name = 'license'
        verbose_name_plural = 'licenses'


class BookManager(models.Manager):
    pass


class Book(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        max_length=255
    )
    isbn = models.CharField(
        verbose_name=_('isbn'),
        max_length=20,
    )
    published_at = models.DateField(
        verbose_name=_('published date')
    )
    author = models.ForeignKey(
        to=Member,
        related_name='book_author',
        on_delete=models.CASCADE
    )
    license = models.ForeignKey(
        to=License,
        related_name='book_license',
        on_delete=models.CASCADE,
    )
    visible = models.BooleanField(
        verbose_name=_('visible'),
        unique=False,
        null=False,
        blank=False,
        default=False
    )

    def __str__(self):
        return self.title

    objects = BookManager()

    class Meta:
        verbose_name = 'book'
        verbose_name_plural = 'books'


class BookPartManager(models.Manager):
    pass


class BookPart(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        max_length=255
    )
    order = models.IntegerField(
        verbose_name=_('order'),
        unique=False,
        null=True,
        blank=True,
        db_index=False
    )
    book = models.ForeignKey(
        to=Book,
        related_name='book_ref',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title

    objects = BookPartManager()

    class Meta:
        verbose_name = 'bookpart'
        verbose_name_plural = 'bookparts'


class PostManager(models.Manager):
    pass


class Post(BaseModel):
    old_slug = models.URLField(
        verbose_name=_('old slug'),
        max_length=2048,
    )
    DRAFT = 'draft'
    PUBLISHED = 'published'
    WARNED = 'warned'
    ARCHIVED = 'archived'
    POST_STATUS_CHOICES = [
        (DRAFT, _('DRAFT')),
        (PUBLISHED, _('PUBLISHED')),
        (WARNED, _('WARNED')),
        (ARCHIVED, _('ARCHIVED'))
    ]
    title = models.CharField(
        verbose_name=_('title'),
        unique=False,
        null=False,
        blank=False,
        max_length=255,
    )
    summary = EditorJSField(
        verbose_name=_('summary'),
        unique=False,
        null=True,
        blank=True,
        max_length=2000,
    )
    bbcode_content = BBCodeTextField(
        verbose_name=_('bbcode content'),
        unique=False,
        null=True,
        blank=True,
    )
    content = EditorJSField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    status = models.CharField(
        verbose_name=_('status'),
        choices=POST_STATUS_CHOICES,
        max_length=20,
        default=DRAFT
    )
    hits_counter = models.IntegerField(
        verbose_name=_('hits count'),
        default=0
    )
    revisions_counter = models.IntegerField(
        verbose_name=_('revisions count'),
        default=0
    )
    validated_at = models.DateTimeField(
        verbose_name=_('validated at'),
        unique=False,
        null=True,
        blank=False
    )
    validated_by = models.ForeignKey(
        to=Member,
        on_delete=models.DO_NOTHING,
        related_name="validated_by",
        null=True,
    )
    author = models.ForeignKey(
        to=Member,
        related_name='post_author',
        on_delete=models.CASCADE
    )
    readings = models.ManyToManyField(
        to=Member
    )
    book_part = models.ForeignKey(
        to=BookPart,
        related_name='book_part_ref',
        on_delete=models.CASCADE,
        null=True,
    )
    tags = models.ManyToManyField(
        to=Tag
    )
    revision = models.ForeignKey(
        to='self',
        related_name='revision_ref',
        on_delete=models.CASCADE,
        null=True
    )
    section = models.ForeignKey(
        to=Section,
        related_name='section_ref',
        on_delete=models.CASCADE
    )

    objects = PostManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'


class CommentManager(models.Manager):
    pass


class Comment(BaseModel):
    author = models.ForeignKey(
        to=Member,
        related_name='comment_author',
        on_delete=models.CASCADE
    )
    content = EditorJSField(
        verbose_name=_('content')
    )
    reply_to = models.ForeignKey(
        to='self',
        related_name='comment_reply_to',
        on_delete=models.CASCADE
    )
    readings = models.ManyToManyField(
        to=Member
    )
    objects = CommentManager()


class Rating(models.Model):
    level = models.PositiveSmallIntegerField(
        verbose_name=_('level'),
        unique=False,
        null=False,
        blank=False,
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )
    owner = models.ForeignKey(
        verbose_name=_('owner'),
        to=Member,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True


class PostRatingManager(models.Manager):
    pass


class PostRating(BaseModel, Rating):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    objects = PostRatingManager()


class CommentRatingManager(models.Manager):
    pass


class CommentRating(BaseModel, Rating):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )
    objects = CommentRatingManager()


class Like(models.Model):
    level = models.PositiveSmallIntegerField(
        verbose_name=_('level'),
        unique=False,
        null=False,
        blank=False,
        default=0,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )
    owner = models.ForeignKey(
        verbose_name=_('owner'),
        to=Member,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )

    class Meta:
        abstract = True


class PostLikeManager(models.Manager):
    pass


class PostLike(BaseModel, Like):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )
    objects = PostLikeManager()


class CommentLikeManager(models.Manager):
    pass


class CommentLike(BaseModel, Like):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )
    objects = CommentLikeManager()


class AdmonitionManager(models.Manager):
    pass


class Admonition(BaseModel):
    subject = models.CharField(
        verbose_name=_('subject'),
        unique=True,
        null=False,
        blank=False,
        db_index=True,
        max_length=255,
        default=_("no subject")
    )
    content = models.TextField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    objects = AdmonitionManager()


class AdmonitionActionManager(models.Manager):
    pass


class AdmonitionAction(BaseModel):
    SYSTEM_ACTION = 'systemAction'
    MESSAGE_TO_USER = 'msgToUser'
    MESSAGE_FROM_USER = 'msgFromUser'
    INTERNAL_MESSAGE = 'internalMsg'
    TYPE_CHOICES = (
        (SYSTEM_ACTION, _('System Action')),
        (MESSAGE_FROM_USER, _('Message from member')),
        (MESSAGE_TO_USER, _('Message to member')),
        (INTERNAL_MESSAGE, _('Internal message'))
    )
    message = models.TextField(
        verbose_name=_('message'),
    )
    type = models.CharField(
        verbose_name=_('type'),
        max_length=30,
        choices=TYPE_CHOICES,
        default=SYSTEM_ACTION
    )
    admonition = models.ForeignKey(
        to=Admonition,
        on_delete=models.CASCADE
    )
    objects = AdmonitionActionManager()


class Alert(models.Model):
    PLAGIARISM = 'plagiarism'
    SPELLING = 'spelling'
    BAD_CATEGORY = 'bad_category'
    HATE = 'hate'
    OTHER = 'other'
    TYPE_ALERT_CHOICES = (
        (PLAGIARISM, _('Plagiarism')),
        (SPELLING, _('Spelling')),
        (BAD_CATEGORY, _('Bad category')),
        (HATE, _('Hate')),
        (OTHER, _('Other'))
    )

    OPEN = 1
    CLOSED = 2
    DISCUSSION = 3
    STATUS_CHOICES = (
        (OPEN, _('open')),
        (CLOSED, _('closed')),
        (DISCUSSION, _('discussion'))
    )

    type = models.CharField(
        verbose_name=_('type'),
        max_length=30,
        choices=TYPE_ALERT_CHOICES,
        default=OTHER
    )
    details = models.TextField(
        verbose_name=_('details'),
        max_length=1000,
        default=""
    )
    status = models.IntegerField(
        verbose_name=_('status'),
        default=1
    )

    class Meta:
        abstract = True


class PostAlertManager(models.Manager):
    pass


class PostAlert(BaseModel, Alert):
    post = models.ForeignKey(
        to=Post,
        on_delete=models.CASCADE
    )

    objects = PostAlertManager()


class CommentAlertManager(models.Manager):
    pass


class CommentAlert(BaseModel, Alert):
    comment = models.ForeignKey(
        to=Comment,
        on_delete=models.CASCADE
    )

    objects = CommentAlertManager()


class ContestManager(models.Manager):
    pass


class Contest(BaseModel):
    name = models.CharField(
        verbose_name=_('name'),
        unique=False,
        null=False,
        blank=False,
        max_length=255,
        db_index=True
    )
    starts_at = models.DateField(
        verbose_name=_('start at'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        validators=[not_passed]
    )
    ends_at = models.DateField(
        verbose_name=_('ends at'),
        unique=False,
        null=False,
        blank=False,
        db_index=True,
        validators=[not_passed]
    )
    objects = ContestManager()


class CorrectionRequestManager(models.Manager):
    pass


class CorrectionRequest(BaseModel):
    title = models.CharField(
        verbose_name=_('title'),
        unique=False,
        null=False,
        blank=False,
        max_length=255,
    )
    summary = EditorJSField(
        verbose_name=_('summary'),
        unique=False,
        null=True,
        blank=True,
        max_length=2000,
    )
    bbcode_content = BBCodeTextField(
        verbose_name=_('bbcode content'),
        unique=False,
        null=True,
        blank=True,
    )
    content = EditorJSField(
        verbose_name=_('content'),
        unique=False,
        null=True,
        blank=True,
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.DO_NOTHING
    )
    objects = CorrectionRequestManager()


class CorrectionRequestActionManager(models.Manager):
    pass


class CorrectionRequestAction(BaseModel):
    CORRECTION = 1
    VALIDATION = 2
    ACTION_CHOICES = (
        (CORRECTION, _('Correction')),
        (VALIDATION, _('Validation'))
    )
    owner = models.ForeignKey(
        to=Member,
        on_delete=models.DO_NOTHING
    )
    correction_request = models.ForeignKey(
        to=CorrectionRequest,
        on_delete=models.DO_NOTHING
    )
    action = models.CharField(
        verbose_name=_('action'),
        max_length=30,
        choices=ACTION_CHOICES,
        default=CORRECTION
    )

    objects = CorrectionRequestActionManager()

    class Meta:
        verbose_name = 'Correction Request'
        verbose_name_plural = 'Correction Requests'


class PostListManager(models.Manager):
    pass


class PostList(BaseModel):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=255,
        null=True
    )
    owner = models.ForeignKey(
        to=Member,
        on_delete=models.CASCADE
    )
    posts = models.ManyToManyField(
        to=Post
    )
    removable = models.BooleanField(
        verbose_name=_('removable'),
        default=True
    )
    public = models.BooleanField(
        verbose_name=_('public'),
        default=False
    )

    FAVOURITE_TYPE = 1
    READING_LIST_TYPE = 2
    TYPE_CHOICES = (
        (FAVOURITE_TYPE, _('Favourite')),
        (READING_LIST_TYPE, _('Reading'))
    )
    type = models.IntegerField(
        verbose_name=_('type'),
        choices=TYPE_CHOICES,
        default=READING_LIST_TYPE
    )

    objects = PostListManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Post List'
        verbose_name_plural = 'Post Lists'


class FaqManager(models.Manager):
    pass


class Faq(BaseModel):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    FAQ_STATUS_CHOICES = [
        (DRAFT, _('DRAFT')),
        (PUBLISHED, _('PUBLISHED')),
    ]

    order = models.IntegerField(
        verbose_name=_('order')
    )
    question = models.CharField(
        verbose_name=_('question'),
        max_length=2048,
        null=True
    )
    answer = models.TextField(
        verbose_name=_('answer')
    )

    objects = FaqManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'


class VotingManager(models.Manager):
    pass


class Voting(BaseModel):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=200
    )

    objects = VotingManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Voting'
        verbose_name_plural = 'Votings'


class VotingRoundManager(models.Manager):
    pass


class VotingRound(BaseModel):
    order = models.IntegerField(
        verbose_name=_('order'),
        unique=True,
        null=False,
        blank=False
    )
    voting = models.ForeignKey(
        to=Voting,
        on_delete=models.CASCADE
    )

    objects = VotingRoundManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Voting Round'
        verbose_name_plural = 'Voting Rounds'


class VoteManager(models.Manager):
    pass


class Vote(BaseModel):
    round = models.IntegerField(
        verbose_name=_('round')
    )
    owner = models.ForeignKey(
        to=Member,
        on_delete=models.DO_NOTHING
    )
    post = models.ForeignKey(
        to=Post,
        on_delete=models.DO_NOTHING
    )
    voting_round = models.ForeignKey(
        to=VotingRound,
        on_delete=models.DO_NOTHING
    )

    objects = VoteManager()

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'Vote'
        verbose_name_plural = 'Votes'
