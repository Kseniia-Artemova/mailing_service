from django.template import Library
from mailing.models import Client

register = Library()


@register.filter
def last_name(object):
    if isinstance(object, Client):
        return object.name.split()[0]


@register.filter
def first_name(object):
    if isinstance(object, Client):
        return object.name.split()[1]


@register.filter
def father_name(object):
    if isinstance(object, Client):
        name = object.name.split()
        if len(name) == 3:
            return name[2]
