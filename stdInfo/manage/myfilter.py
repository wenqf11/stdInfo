__author__ = 'vince'
from django import template
register = template.Library()

@register.filter
def key(d, key_name):
    value = ''
    try:
        value = d[key_name]
    except KeyError:
        value = ''
    return value

register.filter('key', key)