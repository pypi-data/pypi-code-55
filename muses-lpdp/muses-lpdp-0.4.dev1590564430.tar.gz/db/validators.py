from datetime import date, datetime

from django.core.exceptions import ValidationError


def not_passed(value: date):
    if not ((value - datetime.now()).total_seconds() > 0):
        raise ValidationError('%(value)s is passed', params={'value': value})


def required_age(value: date, limit_value: int):
    today = date.today()
    try:
        birthday = value.replace(year=today.year)
    except ValueError:
        birthday = value.replace(year=today.year, month=value.month + 1, day=1)
    if birthday > limit_value:
        raise ValidationError('%(value)s is not the required age. %(limit)s expected',
                              params={
                                  'value': value,
                                  'limit': limit_value
                              })
