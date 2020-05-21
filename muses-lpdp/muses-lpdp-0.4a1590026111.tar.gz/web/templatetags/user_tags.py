from django import template

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='in_groups')
def in_groups(user, groups_target):
    for g in user.groups.all():
        return g in groups_target.all()
    return False
