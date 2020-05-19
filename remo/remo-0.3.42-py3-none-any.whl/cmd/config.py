import re
import unicodedata
import warnings
from datetime import datetime
import getpass

import typer
from django.contrib.auth import get_user_model

from remo_app.config.config import Config


def normalize_email(email):
    """
    Normalize the email address by lowercasing the domain part of it.
    """
    email = email or ''
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError:
        pass
    else:
        email = email_name + '@' + domain_part.lower()
    return email


def normalize_username(username):
    return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username


def normalize_user_info(user_name='', email='', password=''):
    if not user_name:
        user_name = getpass.getuser()

    if user_name[0].islower():
        user_name = user_name.capitalize()

    first_name = user_name

    username = re.sub(r"[\s-]+", "_", user_name.lower())
    username = re.sub(r"[^.\w\d_]+", "", username)

    if not password:
        password = 'adminpass'

    if not email:
        email = '{}@remo.ai'.format(username)

    email = normalize_email(email)
    username = normalize_username(username)
    return first_name, username, email, password


def create_or_update_user(user_name='', email='', password=''):
    first_name, username, email, password = normalize_user_info(user_name, email, password)

    User = get_user_model()
    user = User.objects.filter(is_superuser=True).first()
    warnings.simplefilter("ignore")
    if not user:
        user = User.objects.create_superuser(username, email, password, last_login=datetime.now())
        user.first_name = first_name
    else:
        user.first_name = first_name
        user.email = User.objects.normalize_email(email)
        user.username = User.objects.model.normalize_username(username)
        user.set_password(password)
    user.save()

    print(
        f"""
    Remo user:

    login: {email}
    password: {password}
    """
    )

    return first_name, email, password


def create_config(db_url):
    typer.echo('\n-----------------------------------------------\n[-] Creating remo config')
    typer.echo('* Config file location: {}'.format(Config.path()))

    cfg = Config.load()
    if not cfg:
        name, email, password = create_or_update_user()
        cfg = Config(db_url=db_url, user_name=name, user_email=email, user_password=password)
    else:
        name, email, password = create_or_update_user(cfg.user_name, cfg.user_email, cfg.user_password)
        cfg.update(db_url=db_url, user_name=name, user_email=email, user_password=password)
    cfg.save()
    return cfg
